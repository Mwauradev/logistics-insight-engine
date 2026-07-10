from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

def generate_logistics_insight(data: dict) -> str:
    
    prompt = f"""
    You are a logistics operations consultant. Analyze this fleet 
    performance data and write a 5-6 sentence executive insight.
    
    Focus specifically on:
    - Cost relative to performance, not just raw numbers
    - Whether problems are route-based or driver-based
    - One clear, actionable recommendation
    
    Be direct. Avoid generic statements. Point to specific routes, 
    drivers, or vehicles where relevant.Do not include specific percentage savings estimates 
    unless they are directly calculated from the data provided.

    CRITICAL RULES:
    - Use ONLY the exact numbers provided in the data below
    - Do not calculate or estimate any figures not explicitly given
    - Do not invent percentages, costs, or averages
    - If you reference a number, it must appear exactly in the data provided

    
    Fleet Data:
    - Overall Delivery Rate: {data['overall_delivery_rate']}%
    - Total Fuel Cost: KES {data['total_fuel_cost']:,}
    - Total Distance: {data['total_distance']:,} km
    - Average Delay: {data['avg_delay_minutes']} minutes
    - Best Route: {data['best_route']}
    - Worst Route: {data['worst_route']}
    - Most Expensive Route: {data['most_expensive_route']}
    - Best Driver: {data['best_driver']}
    - Most Delayed Driver: {data['most_delayed_driver']}
    - Most Efficient Vehicle: {data['most_efficient_vehicle']}
    
    Write in plain English. No bullet points. No headers.
    Just a clean professional paragraph a transport company 
    owner would actually read and act on.
    """
    
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a senior logistics and fleet operations consultant who identifies cost inefficiencies and operational risks."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1024,
        temperature=0.7
    )
    print(f"DEBUG: {response}")
    print(f"DEBUG content: {response.choices[0].message.content}")

    return response.choices[0].message.content