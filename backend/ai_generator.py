import google.generativeai as genai
from typing import List, Optional, Dict, Any

class AIGenerator:
    """Handles interactions with Google's Gemini API for generating responses"""
    
    # Static system prompt to avoid rebuilding on each call
    SYSTEM_PROMPT = """ You are an AI assistant specialized in course materials and educational content with access to a comprehensive search tool for course information.

Search Tool Usage:
- Use the search tool **only** for questions about specific course content or detailed educational materials
- **One search per query maximum**
- Synthesize search results into accurate, fact-based responses
- If search yields no results, state this clearly without offering alternatives

Response Protocol:
- **General knowledge questions**: Answer using existing knowledge without searching
- **Course-specific questions**: Search first, then answer
- **No meta-commentary**:
 - Provide direct answers only — no reasoning process, search explanations, or question-type analysis
 - Do not mention "based on the search results"


All responses must be:
1. **Brief, Concise and focused** - Get to the point quickly
2. **Educational** - Maintain instructional value
3. **Clear** - Use accessible language
4. **Example-supported** - Include relevant examples when they aid understanding
Provide only the direct answer to what was asked.
"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model,
            system_instruction=self.SYSTEM_PROMPT
        )
        self.model_name = model
    
    def generate_response(self, query: str,
                         conversation_history: Optional[str] = None,
                         tools: Optional[List] = None,
                         tool_manager=None) -> str:
        """
        Generate AI response with optional tool usage and conversation context.
        
        Args:
            query: The user's question or request
            conversation_history: Previous messages for context
            tools: Available tools the AI can use
            tool_manager: Manager to execute tools
            
        Returns:
            Generated response as string
        """
        
        # Build prompt with conversation history
        full_prompt = query
        if conversation_history:
            full_prompt = f"Previous conversation:\n{conversation_history}\n\nCurrent question: {query}"
        
        # Since Gemini doesn't have native tool support like Anthropic,
        # we'll simulate it by detecting course-related queries and searching
        if tools and tool_manager:
            # Check if this is a course-related query
            course_keywords = ['course', 'lesson', 'outline', 'chatbot', 'RAG', 'MCP', 
                             'available', 'curriculum', 'topics', 'explain']
            
            if any(keyword.lower() in query.lower() for keyword in course_keywords):
                # Execute search tool
                try:
                    tool_result = tool_manager.execute_tool("search_course_content", query=query)
                    
                    # Add search results to prompt
                    full_prompt = f"Question: {query}\n\nRelevant course information:\n{tool_result}\n\nBased on the above information, provide a comprehensive answer."
                except:
                    pass  # If tool fails, just use regular prompt
        
        # Generate response with Gemini
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0,
                    "max_output_tokens": 800,
                }
            )
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
