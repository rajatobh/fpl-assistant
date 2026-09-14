import chromadb
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="fpl_players")

def load_players_into_chroma(players, positions, teams):
    documents = []
    ids = []

    for player in players:
        name = f"{player['first_name']} {player['second_name']}"
        position = positions[player['element_type']]
        team = teams[player['team']]
        price = player['now_cost'] / 10
        points = player['total_points']
        value = round(points / price, 1) if price > 0 else 0

        doc = f"{name} plays as {position} for {team}. Price: £{price}m. Total points: {points}. Value: {value} points per £1m."
        documents.append(doc)
        ids.append(str(player['id']))
    
    collection.add(documents=documents, ids=ids)
    print(f"✅ Loaded {len(documents)} players into ChromaDB")

def query_fpl_assistant(question: str, players=None, positions=None, teams=None):
    if players and positions and teams:
        docs = []
        for player in players:
            name = f"{player['first_name']} {player['second_name']}"
            position = positions[player['element_type']]
            team = teams[player['team']]
            price = player['now_cost'] / 10
            points = player['total_points']
            value = round(points / price, 1) if price > 0 else 0
            docs.append(f"{name} plays as {position} for {team}. Price: £{price}m. Total points: {points}. Value: {value} points per £1m.")
        
        context = "\n".join(docs)
    else:
        results = collection.query(query_texts=[question], n_results=20)
        context = "\n".join(results['documents'][0])

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"""You are an FPL (Fantasy Premier League) assistant. 
Use the following player data to answer the question.

Player data:
{context}

Question: {question}

Give a helpful, concise answer based on the data provided."""
            }
        ]
    )
        
    return message.content[0].text