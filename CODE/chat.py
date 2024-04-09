from utils.chatutils import AssistantSession
from utils.datamanager import get_companyfilepaths


company_foldernames = ["cycle0.com", "sulzerschmid.ch", "swissto12.com", "tado.com", "vacuumschmelze.com", "varjo.com"] # folders expected at DATA/CRAWLER which contain all the files for each company

# ALL COMPANIES:
# "anticimex.com", "anybotics.com", "beekeeper.io", "bloomfreshglobal.com", "cfp.energy", "cycle0.com", "distran.swiss",\
# "fotokite.com", "frigoveneta.it", "generainc.com", "getyourguide.com", "medimapsgroup.com", "medtrace.dk",\
# "memo-therapeutics.com", "nagibio.ch", "nilt.com", "oncodna.com", "previero.it", "rencompany.nl",\
# "shl-medical.com", "sulzerschmid.ch", "swissto12.com", "tado.com", "vacuumschmelze.com", "varjo.com"

model = "gpt-3.5-turbo"
gpt_name = "SDG expert"
instruction = "You are a sustainable development goals expert. If asked for, answer questions based on the information in the files provided to you."


if __name__ == "__main__":

    # with open('./CODE/key.txt', 'r') as file:
    with open('C:/Users/levin/Documents/IFZ/GitHub/AI-and-Impact-Investing/CODE/key.txt', 'r') as file: # path to the key.txt file
        # Read the entire content of the file
        api_key = file.read()

    for company_foldername in company_foldernames:

        assistant_session = AssistantSession(
            gpt_name=gpt_name,
            model=model,
            instructions=instruction,
            tools=[{"type": "retrieval"}],
            file_paths=get_companyfilepaths(company_foldername),
            api_key=api_key
        )


        assistant_session.chat("Please provide me with a summary of the content of all the files in couple of sentences. I do not wish to go through them one by one.\
                               Just give me a general idea of what they are about.")
        assistant_session.chat("Purely based on the information in the files, which SDGs arguably does the company have in the focus?")
        assistant_session.chat("If you had to, how would you rank these against each other in terms of how prominent they seem to be in the company's self-presentation based on the information provided to you.")
        assistant_session.save(company_foldername)