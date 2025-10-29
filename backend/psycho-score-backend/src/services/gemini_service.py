import google.generativeai as genai
from fastapi import UploadFile, HTTPException
from PIL import Image
import io
import json
from config.settings import settings
from models.schemas import BusinessCardAnalysis


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def _process_image(self, image: UploadFile) -> Image.Image:
        """Process uploaded image and return PIL Image object"""
        try:
            image_data = image.file.read()
            pil_image = Image.open(io.BytesIO(image_data))

            # Convert to RGB if necessary
            if pil_image.mode != "RGB":
                pil_image = pil_image.convert("RGB")

            # Resize if too large (max 4MB for Gemini)
            max_size = (2048, 2048)
            pil_image.thumbnail(max_size, Image.Resampling.LANCZOS)

            return pil_image
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error processing image: {str(e)}"
            )

    def _create_patrick_bateman_prompt(self) -> str:
        """Create the Patrick Bateman analysis prompt"""
        return """
        You are Patrick Bateman from American Psycho. A business card has been presented to you for analysis.

        Analyze this business card image with Patrick Bateman's obsessive attention to detail and pretentious, competitive commentary. Focus on:

        - Typography and font choices
        - Color scheme and sophistication  
        - Layout and design composition
        - Paper quality and material impression
        - Overall aesthetic and attention to detail

        Write your response as Patrick Bateman would speak - sophisticated, obsessive, competitive, and slightly unhinged. 
        Reference specific design elements like you're examining Paul Allen's card. Include comparisons to high-end materials and brands.

        Start with something like "Look at that..." and build your critique in Patrick's voice.

        Then provide your response in JSON format:
        {
            "card_quality": "Brief assessment",
            "design_elements": {
                "layout": "Layout analysis", 
                "whitespace": "Whitespace usage",
                "composition": "Overall composition"
            },
            "typography": {
                "font_family": "Font analysis",
                "hierarchy": "Typography hierarchy", 
                "readability": "Readability assessment"
            },
            "color_scheme": {
                "palette": "Color description",
                "contrast": "Contrast analysis",
                "sophistication": "Color sophistication"
            },
            "layout_quality": "Layout assessment",
            "material_impression": "Material quality perception",
            "patrick_critique": "Your full Patrick Bateman critique in his natural speaking voice, as if he's talking directly to someone. Write this as natural dialogue - conversational, dramatic, and unhinged. Avoid bullet points, lists, or overly structured text. Make it sound like Patrick is actually speaking. 2-3 sentences maximum for better audio flow.",
            "psycho_score": 7.5
        }

        The psycho_score should be 0-10, where 10 is impossible perfection by Patrick's standards.
        IMPORTANT: For the patrick_critique field, write ONLY natural speech - no formatting, no bullet points, no special characters. Write as if Patrick is speaking directly to someone about the card DO NOT ADD ANY MARKDOWN OR FORMATTING SUCH AS BOLD TEXT.
        """

    async def analyze_business_card(self, image: UploadFile) -> BusinessCardAnalysis:
        """Analyze business card using Gemini Vision API"""
        try:
            # Process the image
            pil_image = self._process_image(image)

            # Create the prompt
            prompt = self._create_patrick_bateman_prompt()

            # Generate content with Gemini
            response = self.model.generate_content([prompt, pil_image])

            # Parse the JSON response
            try:
                # Extract JSON from response text
                response_text = response.text
                # Remove any markdown formatting
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0]

                analysis_data = json.loads(response_text.strip())

                # Validate and create BusinessCardAnalysis object
                return BusinessCardAnalysis(**analysis_data)

            except json.JSONDecodeError:
                # Fallback: create a basic analysis if JSON parsing fails
                return self._create_fallback_analysis(response.text)

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error analyzing business card: {str(e)}"
            )

    def _create_comparison_prompt(self) -> str:
        """Create the Patrick Bateman comparison prompt for two business cards"""
        return """
        You are Patrick Bateman from American Psycho. Two business cards have been presented to you for a COMPETITIVE ANALYSIS.

        You must analyze both cards with your obsessive attention to detail and determine which one is superior. This is a BATTLE of sophistication, taste, and professional excellence.

        Analyze both cards focusing on:
        - Typography and font sophistication 
        - Color scheme elegance and restraint
        - Layout composition and balance
        - Paper quality perception
        - Overall aesthetic superiority
        - Attention to design details

        Write your response as Patrick Bateman would speak during a heated business card comparison scene - competitive, obsessive, and increasingly unhinged as you dissect every detail.

        After your analysis, you MUST declare one card as "ALPHA" (superior) and the other as "BETA" (inferior).

        Provide your response in JSON format:
        {
            "card1_analysis": {
                "strengths": "What makes this card impressive",
                "weaknesses": "What disappoints you about this card", 
                "psycho_score": 7.2
            },
            "card2_analysis": {
                "strengths": "What makes this card impressive",
                "weaknesses": "What disappoints you about this card",
                "psycho_score": 8.1
            },
            "comparison_critique": "Your full Patrick Bateman comparison in his voice - be dramatic, competitive, and unhinged (3-4 paragraphs)",
            "winner": "ALPHA",
            "winner_reasoning": "Why this card dominates the other",
            "final_verdict": "ALPHA"
        }

        The winner and final_verdict should be either "ALPHA" (for the first/original card) or "BETA" (for the second/contender card).
        Psycho_scores should be 0-10, where 10 is impossible perfection.
        DO NOT FORMAT YOUR RESPONSE, ONLY GENERATE PLAIN TEXT without bold or markdown.
        """

    async def compare_business_cards(
        self, original_image: UploadFile, contender_image: UploadFile
    ) -> dict:
        """Compare two business cards and determine ALPHA vs BETA"""
        try:
            # Process both images
            original_pil = self._process_image(original_image)
            contender_pil = self._process_image(contender_image)

            # Create the comparison prompt
            prompt = self._create_comparison_prompt()

            # Generate content with Gemini using both images
            response = self.model.generate_content(
                [
                    "ORIGINAL CARD (Judge this as Card 1):",
                    original_pil,
                    "CONTENDER CARD (Judge this as Card 2):",
                    contender_pil,
                    prompt,
                ]
            )

            # Parse the JSON response
            try:
                response_text = response.text
                # Remove any markdown formatting
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0]

                comparison_data = json.loads(response_text.strip())
                return comparison_data

            except json.JSONDecodeError:
                # Fallback comparison if JSON parsing fails
                return self._create_fallback_comparison(response.text)

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error comparing business cards: {str(e)}"
            )

    def _create_fallback_comparison(self, raw_response: str) -> dict:
        """Create a fallback comparison if JSON parsing fails"""
        return {
            "card1_analysis": {
                "strengths": "Professional presentation detected",
                "weaknesses": "Standard execution",
                "psycho_score": 6.5,
            },
            "card2_analysis": {
                "strengths": "Competent design approach",
                "weaknesses": "Lacks distinctive edge",
                "psycho_score": 6.8,
            },
            "comparison_critique": raw_response[:800]
            if raw_response
            else "The comparison reveals subtle differences in execution. While both cards demonstrate professional competence, one shows marginally superior attention to detail and aesthetic refinement.",
            "winner": "BETA",
            "winner_reasoning": "Slight edge in overall composition and sophistication",
            "final_verdict": "BETA",
        }

    def _create_fallback_analysis(self, raw_response: str) -> BusinessCardAnalysis:
        """Create a fallback analysis if JSON parsing fails"""
        return BusinessCardAnalysis(
            card_quality="Analysis completed with standard processing",
            design_elements={
                "layout": "Professional layout detected",
                "whitespace": "Adequate spacing",
                "composition": "Standard business card composition",
            },
            typography={
                "font_family": "Standard business fonts",
                "hierarchy": "Clear hierarchy",
                "readability": "Good readability",
            },
            color_scheme={
                "palette": "Professional color scheme",
                "contrast": "Adequate contrast",
                "sophistication": "Business appropriate",
            },
            layout_quality="Professional standard",
            material_impression="Standard business card stock",
            patrick_critique=raw_response[:500]
            if raw_response
            else "The subtlety of the design shows a certain... restraint. Though lacking the sophisticated edge I prefer in my own cards, it demonstrates a basic understanding of professional presentation.",
            psycho_score=6.5,
        )


# Create global instance
gemini_service = GeminiService()
