from datadreamer import DataDreamer
from datadreamer.llms import OpenAI
from datadreamer.steps import ProcessWithPrompt, HFHubDataSource, CSVDataSource, DataFromPrompt
with DataDreamer("./output"):
    # Load GPT-4
    gpt_4 = OpenAI(model_name="gpt-4")

    # load csv of employees
    employees = CSVDataSource(
        "load employees",
        "DB/output",
        "joined_data.csv",
        split="train"
    ).select_columns(['first_name', 'last_name', 'role', 'skill', 'proficiency_lvl'])

    more_employees = DataFromPrompt(
        "Generate synthetic data based on given csv",
        inputs={"inputs": employees.output['first_name', 'last_name', 'role', 'skill', 'proficiency_lvl']},
        args={
            "llm": gpt_4,
            "instruction": (
                "Given the dataset generate more synthetic data based on the roles and skills."
                "Return only the extended dataset, nothing else."
            ),
        },
        outputs={
            "inputs": "employee dataset", 
            "generations": "extended dataset"},
    ).select_columns(["questions", "decompositions"])
    
    print(more_employees)