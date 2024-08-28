#### Restarting/Connecting to MySQL
```"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld" --console```

Properties
- localhost 3306
- user: root
- password: 1234
- database: mysql

#### Postgres SQL 
```docker run --name some-postgres -e POST-GRES_PASSWORD=mysecretpassword -p 5432:5432 -v D:\postgres-data:/var/lib/postgresql/data -d postgres```  
1. Create skill tabel  
`create table skills (
skill_id SERIAL PRIMARY KEY,
skill VARCHAR(100)
)`
2. Create role tabel  
`create table roles (
role_id SERIAL PRIMARY KEY,
role VARCHAR(100)
)`  
3. Create employee tabel  
`create table employees (
employee_id SERIAL PRIMARY KEY,
first_name VARCHAR(50),
last_name VARCHAR(50),
role_id int references roles(role_id)
)`
4. Create Proficiency Level  
`CREATE TYPE proficiency AS ENUM ('BEGINNER', 'INTERMEDIATE', 'PROFESSIONAL')
create table employee_skills (
employee_id int references employees(employee_id),
skill_id int references skills(skill_id),
proficiency_lvl proficiency
)`  
5. Run script `DB/dbGenerate.py`

# Run Pipeline
1. open the Thesis folder in a terminal (not the IDE terminal, if it doesn't support cursors)
2. activate venv `venv\Scripts\activate.bat`
3. run script `python Pipeline\pipeline.py`

# Directory Structure
The project is organized as follows:
### Zero-Shot Classification with the synthesized data
````
.
├── Classification_Synth/  
│   ├── ClassifierOutput/  
│   ├── GroundTruth/  
│   ├── generate.py  
│   ├── truth.py 
│   ├── userStories.csv  
│   └── ZeroShotClassificator.py
````
The `Classification_Synth` Package consists of multiple functions. The center of attention is the
`ZeroShotClassificator.py`. The script uses the synthesized user stories (`userStories.csv`) and the skills of the employee dataset
and does a zero-shot classification. 
In the `ClassifierOutput` the resulting txt and csv files are saved. 
The `Ground Truth` contains resulting metrics (for bart and deberta) in a csv file, which are used for comparison in later stages.

### Zero-Shot Classification with data from the TAWOS database
````
├── Classification_TAWOS/  
│   ├── assets/...  
│   ├── ClassifierOutput/...  
│   ├── final_assets/...  
│   ├── GroundTruth/...  
│   ├── csvConv.py  
│   ├── ExtractAllUserStories.py  
│   ├── ReduceAndGroup.py  
│   ├── ZeroShotClassificatorLooped.py  
│   └── ZeroShotClassificatorTest.py  
````
For this classification data extracted from the TAWOS database through `ExtractAllUserStories.py`. 
It is essential to reduce, group or both through the `ReduceAndGroup.py` script. 
In the assets folder is a `cleaned.csv` (which contains the components reduced by hand) 
as well as a `grouped_comps.yml` file which helps in the grouping process in the `ReduceAndGroup.py` script
The `final_asstets` folder contains the user stories and the components after reducing/grouping which are used for the 
zero-shot classification as well as the output_csv and output_txts.

### Zero-Shot Classification with data from the TAWOS database and the skills from the employee database before and after fine-tuning
````
├── Classification_TAWOS_Synth/  
│   ├── assets  
│   ├── PostFineTuning  
│   ├── PreFineTuning  
│   ├── compare_two_prediction_sets.py
│   ├── display_entailments.py
│   ├── generate_metrics_table.py
│   ├── plots_histogram.py  
│   ├── select_random_user_stories.py
│   ├── sort_data.py  
│   ├── truth.csv
│   └── Zero_Shot_Classification.py
````
The assets folder contains a csv file which contains 25 random user stories (origning from TAWOS). These are randomly 
selected through the `select_random_user_stories.py` script.  
The `PostFineTuning` and `PreFineTuning` Folders contain the resulting predictions of the `Zero_Shot_Classification.py` script.
Other than that, the folder contains different scripts for generating metrics or evaluations.

### Development of the employee database
````
├── DB/
│   ├── datasets
│   ├── GenerationOfStories
│   ├── output
│   ├── addDescription.py
│   ├── csvGenerator.py
│   ├── dbGenerate.py
│   └── generateSkillTable.py
````
The DB folder represents the code, which was used to create the employee database.
Therefore, there were a csv files for:
- random names, 
- a batch of [roles and role descriptions](https://www.kaggle.com/datasets/anujrajawat/itjobs-and-skills), 
- a portion of the [roles](https://www.kaggle.com/datasets/anujrajawat/itjobs-and-skills) and which were matches with [skills](https://www.kaggle.com/datasets/zamamahmed211/skills) -> matched manually
- a batch of [skills](https://www.kaggle.com/datasets/zamamahmed211/skills)

The `dbGenerate.py` script generates the data for the employee database. The setup of the database, 
if no dump is available is described in [here](#postgres-sql-)

### Fine-Tuning
````
├── FineTuning/
│   ├── FinalRuns
│   ├── FinalRuns_PreTrained
│   ├── FinalRuns_PreTrained_bart
│   ├── FinalRuns_PreTrained_deberta
│   ├── output_csv
│   ├── output_txt
│   ├── finetuning-Trainer.ipynb
│   ├── metrics.py
│   └── truth.csv
````
The Fine-Tuning contains the resulting models from the Fine-Tuning runs as well as the predictions outputs of a zero shot classification with the new models.
In the `fine_tuning.ipynb` is the preparation and the actual fine-tuning located as well as a zero-shot classification

### Pipeline
````
├── Pipeline
    └── pipeline.py
````
The `pipeline` script allows users to select a model, input a user story, 
and perform zero-shot classification on a predefined set of skills. Based on the positively classified (entailment) skills, 
the script can filter individuals who are proficient in those specific skills.

![pipeline_flowchart.png](Pipeline/pipeline_flowchart.png)
