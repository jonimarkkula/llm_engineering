import gradio as gr
import threading
import time
from deal_agent_framework import DealAgentFramework
from agents.deals import Opportunity, Deal


class App:

    def __init__(self):    
        self.agent_framework = None

    def run(self):
        with gr.Blocks(title="The Price is Right", fill_width=True) as ui:

            def table_for(opps):
                """Convert Opportunity objects into table rows."""
                return [
                    [
                        opp.deal.product_description,
                        f"${opp.deal.price:.2f}",
                        f"${opp.estimate:.2f}",
                        f"${opp.discount:.2f}",
                        opp.deal.url
                    ]
                    for opp in opps
                ]

            def get_latest_opps():
                """Return the latest opportunities from memory."""
                if self.agent_framework and self.agent_framework.memory:
                    opportunities = self.agent_framework.memory
                    return table_for(opportunities)
                return []

            def start():
                """Initialize the agent framework and start background updates."""
                self.agent_framework = DealAgentFramework()
                self.agent_framework.init_agents_as_needed()

                # Start background scheduler thread after initialization
                threading.Thread(target=background_scheduler, daemon=True).start()

                return get_latest_opps()

            def background_scheduler():
                """Run the agent every 60 seconds in the background."""
                while True:
                    try:
                        if self.agent_framework:
                            self.agent_framework.run()
                        else:
                            print("Agent framework not initialized yet.")
                    except Exception as e:
                        print(f"Background scheduler error: {e}")
                    time.sleep(60)

            def do_select(selected_index: gr.SelectData):
                opportunities = self.agent_framework.memory
                row = selected_index.index[0]
                opportunity = opportunities[row]
                self.agent_framework.planner.messenger.alert(opportunity)

            with gr.Row():
                gr.Markdown(
                    '<div style="text-align: center;font-size:24px">'
                    '"The Price is Right" - Deal Hunting Agentic AI</div>'
                )
            with gr.Row():
                gr.Markdown(
                    '<div style="text-align: center;font-size:14px">'
                    'Autonomous agent framework that finds online deals, '
                    'collaborating with a proprietary fine-tuned LLM deployed on Modal, '
                    'and a RAG pipeline with a frontier model and Chroma.'
                    '</div>'
                )
            with gr.Row():
                gr.Markdown(
                    '<div style="text-align: center;font-size:14px">'
                    'Deals surfaced so far:'
                    '</div>'
                )
            with gr.Row():
                opportunities_dataframe = gr.Dataframe(
                    headers=["Description", "Price", "Estimate", "Discount", "URL"],
                    wrap=True,
                    column_widths=[4, 1, 1, 1, 2],
                    row_count=10,
                    col_count=5,
                    max_height=400,
                )

            ui.load(start, inputs=[], outputs=[opportunities_dataframe])

            timer = gr.Timer(value=10)
            timer.tick(fn=get_latest_opps, inputs=[], outputs=[opportunities_dataframe])

            opportunities_dataframe.select(do_select)

        ui.launch(share=False, inbrowser=True)


if __name__ == "__main__":
    App().run()
