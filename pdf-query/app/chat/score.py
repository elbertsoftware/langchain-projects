import random

from app.chat.redis import client  # choosing redis for simplicity of increasing numbers by an amount


def random_component_by_score(component_type, component_map):
    # check for valid component type
    if component_type not in ['llm', 'memory', 'retriever']:
        raise ValueError('Invalid component_type')
    
    # from redis, get the hash containing the sum total scores for the the given component_type
    values = client.hgetall(f'{component_type}_score_values')

    # from redis, get the hash containing the number of times each component has been voted on
    counts = client.hgetall(f'{component_type}_score_counts')
    # print(values, counts)

    # get all the valid component names from the component_map
    names = component_map.keys()  # to be sure accessing currently in use component rather stall data from redis

    # loop over those valid names and use them to calculate the average score for each
    scores = {}
    for name in names:
        value = int(values.get(name, 1))  # redis stores numbers as strings
        count = int(counts.get(name, 1))  # if a component has not been voted yet, default value is 1

        # add average score to a dictionary
        # avoid down vote which could prevent selecting the component again, default zero score to 0.1
        scores[name] = max(value / count, 0.1)

    print(scores)

    # do a weighted random selection
    sum_scores = sum(scores.values())
    random_value = random.uniform(0, sum_scores)

    cumulative = 0
    for name, value in scores.items():
        cumulative += value
        if random_value <= cumulative:
            return name

def score_conversation(conversation_id: str, score: float, llm: str, retriever: str, memory: str) -> None:
    """
    This function interfaces with langfuse to assign a score to a conversation, specified by its ID.
    It creates a new langfuse score utilizing the provided llm, retriever, and memory components.
    The details are encapsulated in JSON format and submitted along with the conversation_id and the score.

    :param conversation_id: The unique identifier for the conversation to be scored.
    :param score: The score assigned to the conversation.
    :param llm: The Language Model component information.
    :param retriever: The Retriever component information.
    :param memory: The Memory component information.

    Example Usage:

    score_conversation('abc123', 0.75, 'llm_info', 'retriever_info', 'memory_info')
    """

    score = min(max(score, 0), 1)  # make sure score falls b/w 0 and 1

    # hash increase by
    client.hincrby('llm_score_values', llm, score)  # increase value of key 'llm' in the hash 'llm_score_values' by score
    client.hincrby('llm_score_counts', llm, 1)

    client.hincrby('retriever_score_values', retriever, score)
    client.hincrby('retriever_score_counts', retriever, 1)

    client.hincrby('memory_score_values', memory, score)
    client.hincrby('memory_score_counts', memory, 1)


def get_scores():
    """
    Retrieves and organizes scores from the langfuse client for different component types and names.
    The scores are categorized and aggregated in a nested dictionary format where the outer key represents
    the component type and the inner key represents the component name, with each score listed in an array.

    The function accesses the langfuse client's score endpoint to obtain scores.
    If the score name cannot be parsed into JSON, it is skipped.

    :return: A dictionary organized by component type and name, containing arrays of scores.

    Example:

        {
            'llm': {
                'chatopenai-3.5-turbo': [score1, score2],
                'chatopenai-4': [score3, score4]
            },
            'memory': { 'persist_memory': [score7, score8] },
            'retriever': { 'pinecone_store': [score5, score6] }            
        }
    """

    aggregate = {
        'llm': {},
        'memory': {},
        'retriever': {}
    }

    for component_type in aggregate.keys():
        values = client.hgetall(f'{component_type}_score_values')
        counts = client.hgetall(f'{component_type}_score_counts')

        names = values.keys()
        for name in names:
            value = int(values.get(name, 1))
            count = int(counts.get(name, 1))

            score = value / count
            aggregate[component_type][name] = [score]


    return aggregate