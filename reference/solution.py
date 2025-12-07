#!/usr/bin/env python3
"""Multi-context pizza ordering agent.

Lab 2.5 Deliverable: Demonstrates context-based workflows with three
contexts (greeting, ordering, checkout) and context switching.
"""

from signalwire_agents import AgentBase, SwaigFunctionResult


class PizzaAgent(AgentBase):
    """Pizza ordering agent with multi-context workflow."""

    MENU = {
        "margherita": 12.99,
        "pepperoni": 14.99,
        "veggie": 13.99,
        "meat lovers": 16.99,
        "hawaiian": 14.99,
        "supreme": 17.99
    }

    SIZES = {
        "small": 0,
        "medium": 2,
        "large": 4
    }

    def __init__(self):
        super().__init__(name="pizza-agent")

        self.prompt_add_section(
            "Role",
            "You are a pizza ordering assistant for Pizza Palace."
        )

        self.prompt_add_section(
            "Guidelines",
            bullets=[
                "Be friendly and helpful",
                "Confirm orders before checkout",
                "Suggest popular items if asked"
            ]
        )

        self.add_language("English", "en-US", "rime.spore")

        self._setup_contexts()
        self._setup_functions()

    def _setup_contexts(self):
        """Define workflow contexts using SDK context system."""
        contexts = self.define_contexts()

        # Greeting context - entry point
        greeting = contexts.add_context("greeting")
        greeting.add_step("welcome") \
            .set_text(
                "Welcome to Pizza Palace! Would you like to hear our menu "
                "or start ordering?"
            ) \
            .set_step_criteria("Customer has indicated they want to order or hear menu") \
            .set_valid_steps(["next"])
        greeting.add_step("ready") \
            .set_text("Ready to take your order when you are!") \
            .set_functions(["get_menu", "start_order"])

        # Ordering context - pizza selection
        ordering = contexts.add_context("ordering")
        ordering.add_step("select") \
            .set_text("What pizza would you like to order?") \
            .set_step_criteria("Customer has selected pizzas or wants to checkout") \
            .set_functions(["add_pizza", "finish_order", "get_menu", "remove_last_item"])

        # Checkout context - confirmation
        checkout = contexts.add_context("checkout")
        checkout.add_step("confirm") \
            .set_text("Please confirm your order.") \
            .set_functions(["confirm_order", "cancel_order", "add_more"])

    def _setup_functions(self):
        """Define SWAIG functions for all contexts."""

        @self.tool(description="Get the pizza menu")
        def get_menu(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            menu_items = [f"{name.title()}: ${price}" for name, price in self.MENU.items()]
            sizes = [f"{size.title()}: +${upcharge}" for size, upcharge in self.SIZES.items() if upcharge > 0]
            return SwaigFunctionResult(
                f"Our pizzas: {', '.join(menu_items)}. "
                f"Size upcharges: {', '.join(sizes)}. Small has no upcharge."
            )

        @self.tool(description="Start a new pizza order")
        def start_order(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            return (
                SwaigFunctionResult("Great! What pizza would you like?")
                .swml_change_context("ordering")
                .update_global_data({"order_started": True, "items": []})
            )

        @self.tool(
            description="Add a pizza to the order",
            parameters={
                "type": "object",
                "properties": {
                    "pizza_type": {
                        "type": "string",
                        "enum": list(self.MENU.keys()),
                        "description": "Type of pizza"
                    },
                    "size": {
                        "type": "string",
                        "enum": list(self.SIZES.keys()),
                        "description": "Pizza size"
                    }
                },
                "required": ["pizza_type", "size"]
            }
        )
        def add_pizza(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            pizza_type = args.get("pizza_type", "")
            size = args.get("size", "medium")
            raw_data = raw_data or {}
            global_data = raw_data.get("global_data", {})
            items = global_data.get("items", [])

            base_price = self.MENU.get(pizza_type, 0)
            size_upcharge = self.SIZES.get(size, 0)
            price = base_price + size_upcharge

            items.append({
                "type": pizza_type,
                "size": size,
                "price": price
            })

            return (
                SwaigFunctionResult(
                    f"Added {size} {pizza_type} pizza (${price:.2f}). "
                    f"You have {len(items)} item(s). Would you like anything else?"
                )
                .update_global_data({"items": items})
            )

        @self.tool(description="Remove the last item from the order")
        def remove_last_item(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            raw_data = raw_data or {}
            global_data = raw_data.get("global_data", {})
            items = global_data.get("items", [])

            if not items:
                return SwaigFunctionResult("Your cart is empty.")

            removed = items.pop()
            return (
                SwaigFunctionResult(
                    f"Removed {removed['size']} {removed['type']}. "
                    f"You have {len(items)} item(s) remaining."
                )
                .update_global_data({"items": items})
            )

        @self.tool(description="Finish ordering and proceed to checkout")
        def finish_order(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            raw_data = raw_data or {}
            global_data = raw_data.get("global_data", {})
            items = global_data.get("items", [])

            if not items:
                return SwaigFunctionResult(
                    "Your cart is empty. What pizza would you like?"
                )

            total = sum(item["price"] for item in items)
            order_summary = ", ".join(
                f"{item['size']} {item['type']}" for item in items
            )

            return (
                SwaigFunctionResult(
                    f"Your order: {order_summary}. "
                    f"Total: ${total:.2f}. Ready to checkout?"
                )
                .swml_change_context("checkout")
                .update_global_data({"total": total})
            )

        @self.tool(description="Confirm and place the order")
        def confirm_order(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            raw_data = raw_data or {}
            global_data = raw_data.get("global_data", {})
            total = global_data.get("total", 0)
            items = global_data.get("items", [])

            order_summary = ", ".join(
                f"{item['size']} {item['type']}" for item in items
            )

            return (
                SwaigFunctionResult(
                    f"Order confirmed! {order_summary}. "
                    f"Total: ${total:.2f}. Ready in 20 minutes. Thank you!"
                )
                .update_global_data({"order_confirmed": True})
            )

        @self.tool(description="Cancel the order")
        def cancel_order(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            return (
                SwaigFunctionResult("Order cancelled. Come back anytime!")
                .update_global_data({"items": [], "total": 0})
                .swml_change_context("greeting")
            )

        @self.tool(description="Go back to add more items")
        def add_more(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            return (
                SwaigFunctionResult("Sure! What else would you like?")
                .swml_change_context("ordering")
            )


if __name__ == "__main__":
    agent = PizzaAgent()
    agent.run()
