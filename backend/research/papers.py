PAPERS = [
    {
        "title": "Overfishing and Climate Drives Changes in Biology and Recruitment of the Indian Oil Sardine",
        "topics": [
            "Indian Oil Sardine",
            "Sardinella longiceps",
            "sea surface temperature",
            "climate",
            "fish recruitment"
        ],
        "finding": (
            "Climate-related environmental changes, including "
            "sea surface temperature variation, can influence "
            "the biology and recruitment of Indian oil sardine."
        )
    },

    {
        "title": "Satellite chlorophyll concentration as an aid to understanding the dynamics of Indian oil sardine in the southeastern Arabian Sea",
        "topics": [
            "Indian Oil Sardine",
            "Sardinella longiceps",
            "chlorophyll",
            "phytoplankton",
            "Arabian Sea"
        ],
        "finding": (
            "Satellite-derived chlorophyll concentration can help "
            "understand the distribution and dynamics of Indian "
            "oil sardine in the southeastern Arabian Sea."
        )
    },

    {
        "title": "Investigating Indian oil sardine aggregation events in coastal waters of the southeastern Arabian Sea",
        "topics": [
            "Indian Oil Sardine",
            "Sardinella longiceps",
            "Arabian Sea",
            "sea surface temperature",
            "phytoplankton",
            "ocean conditions"
        ],
        "finding": (
            "Environmental conditions such as temperature, "
            "phytoplankton and oceanographic processes are "
            "associated with Indian oil sardine aggregation events."
        )
    }
]


def search_papers(query):

    query = query.lower()

    results = []

    for paper in PAPERS:

        score = 0

        for topic in paper["topics"]:

            if topic.lower() in query:
                score += 1

        if score > 0:

            results.append({
                "title": paper["title"],
                "finding": paper["finding"],
                "relevance_score": score
            })

    results.sort(
        key=lambda x: x["relevance_score"],
        reverse=True
    )

    return results[:3]

if __name__ == "__main__":
    results = search_papers(
        "Indian Oil Sardine sea surface temperature chlorophyll"
    )

    for paper in results:
        print("\nTITLE:", paper["title"])
        print("FINDING:", paper["finding"])
        print("SCORE:", paper["relevance_score"])