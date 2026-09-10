def create_chat_response(result):

    species = result["species"]

    risk = result["final_risk"]["overall_risk"]
    confidence = result["final_risk"]["confidence"]

    reasoning = result["reasoning"]["reasoning"]

    response = f"🐋 ORCA Marine Ecosystem Analysis\n\n"

    response += f"🐟 Species: {species}\n\n"

    response += f"⚠️ Overall Ecosystem Risk: {risk}\n\n"

    response += f"📊 Confidence: {confidence}%\n\n"

    response += "🧠 Why ORCA reached this conclusion:\n"

    for reason in reasoning:
        response += f"• {reason}\n"

    response += "\n🔎 ORCA combined information from multiple specialist agents."

    return response