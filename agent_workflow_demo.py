from mragent import MRAgent

if __name__ == '__main__':
    mr_key = ''
    AI_key = ''


    # openai
    agent = MRAgent(outcome='back pain', AI_key=AI_key, model='MR',
                    num=50, bidirectional=True, introduction=False, LLM_model='gpt-4o',
                    base_url="https://api.gpt.ge/v1/", gwas_token=mr_key,
                    mr_quality_evaluation=True, mr_quality_evaluation_key_item=['4b', '4e', '6e', '10d'], mrlap=True)
    agent.run(step=[1, 2, 3, 4, 5, 6, 7, 8])
    agent.run(step=[9])
    # agent.run()
