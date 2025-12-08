#!/usr/bin/env python3
"""Lab 2.5: Contexts & Workflows - Starter Template

Complete the TODOs to implement the lab requirements.
"""

from signalwire_agents import AgentBase, SwaigFunctionResult


class PizzaAgent(AgentBase):
    """Pizza ordering agent with multi-context workflow."""

    MENU = {
        "margherita": 12.99,
        "pepperoni": 14.99,
        "veggie": 13.99,
        "meat lovers": 16.99
    }

    SIZES = {
        "small": 0,
        "medium": 2,
        "large": 4
    }

    def __init__(self):
        super().__init__(name="pizza-agent", route="/agent")

        self.prompt_add_section(
            "Role",
            "You are a pizza ordering assistant for Pizza Palace."
        )

        self.add_language("English", "en-US", "rime.spore")

        self._setup_contexts()
        self._setup_functions()

    def _setup_contexts(self):
        """Define workflow contexts using SDK context system."""
        # TODO: Create contexts using self.define_contexts()
        # - greeting: Welcome and menu info
        # - ordering: Pizza selection
        # - checkout: Order confirmation
        #
        # Example:
        # contexts = self.define_contexts()
        # greeting = contexts.add_context("greeting")
        # greeting.add_step("welcome") \
        #     .set_text("Welcome message") \
        #     .set_functions(["get_menu", "start_order"])
        pass

    def _setup_functions(self):
        """Define SWAIG functions for all contexts."""
        # TODO: Create functions using @self.tool decorator:
        # - start_order: Begin the ordering process
        # - add_pizza: Add pizza with type and size parameters
        # - complete_order: Finish ordering and go to checkout
        #
        # Example:
        # @self.tool(description="Start a new pizza order")
        # def start_order(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
        #     return (
        #         SwaigFunctionResult("Great! What pizza would you like?")
        #         .swml_change_context("ordering")
        #     )
        pass


agent = PizzaAgent()

if __name__ == "__main__":
    agent.run()
