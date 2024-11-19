from mragent import MRAgentOE


if __name__ == '__main__':
    mr_key = ''
    AI_key = ''

    # openai
    agent = MRAgentOE(exposure='spondylolysis', outcome='low back pain',
                      AI_key='', LLM_model='gpt-4o',
                      model='MR', synonyms=False, bidirectional=False, introduction=False, gwas_token=mr_key)
    agent.run(step=[1, 2, 3, 4, 5, 6, 7, 8, 9])
