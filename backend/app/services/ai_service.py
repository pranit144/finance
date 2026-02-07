import os
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from ..core.config import settings

class AIService:
    def __init__(self):
        self.groq_api_key = settings.GROQ_API_KEY
        
        # Initialize the financial research agent
        self.phi_agent = Agent(
            name="Stocklyze AI Research Agent",
            model=Groq(id="llama3-70b-8192", api_key=self.groq_api_key),
            tools=[
                DuckDuckGo(),
                YFinanceTools(
                    stock_price=True,
                    analyst_recommendations=True,
                    company_info=True
                )
            ],
            instructions=[
                "You are a highly skilled financial research assistant for Stocklyze.",
                "Provide detailed analysis with insights on the stock performance.",
                "Summarize analyst recommendations (Buy/Hold/Sell).",
                "Include recent news articles with links and brief descriptions.",
                "Mention potential risks and opportunities based on news and trends.",
                "Use markdown formatting for clarity and structure.",
            ],
            show_tool_calls=False,
            markdown=True,
        )

    def get_stock_analysis(self, symbol: str) -> str:
        """
        Runs the AI agent to get detailed financial analysis for a stock.
        """
        prompt = f"Provide comprehensive financial analysis for {symbol}. Include performance metrics, analyst recommendations, key financial ratios explanation, and latest news with their potential impact on the stock price."
        try:
            response = self.phi_agent.run(prompt)
            return response.content
        except Exception as e:
            print(f"Error running AI analysis: {e}")
            return f"Sorry, I couldn't generate an analysis for {symbol} at this moment."

ai_service = AIService()
