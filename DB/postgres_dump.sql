--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:KplN5AqFbQ7EvH8PErLzlg==$MJSQlF86N+6PUhuckmlXCT/XRqN3u+fBg/aQxj5VIig=:Hh/caLahEAjDC0T+h3tMWskpmY/j/cYcF5RokiSrIUI=';

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Debian 16.2-1.pgdg120+2)
-- Dumped by pg_dump version 16.2 (Debian 16.2-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL database dump complete
--

--
-- Database "paper" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Debian 16.2-1.pgdg120+2)
-- Dumped by pg_dump version 16.2 (Debian 16.2-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: paper; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE paper WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE paper OWNER TO postgres;

\connect paper

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Debian 16.2-1.pgdg120+2)
-- Dumped by pg_dump version 16.2 (Debian 16.2-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: proficiency; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.proficiency AS ENUM (
    'BEGINNER',
    'INTERMEDIATE',
    'PROFESSIONAL'
);


ALTER TYPE public.proficiency OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: employee_skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employee_skills (
    employee_id integer,
    skill_id integer,
    proficiency_lvl public.proficiency
);


ALTER TABLE public.employee_skills OWNER TO postgres;

--
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    employee_id integer NOT NULL,
    first_name character varying(50),
    last_name character varying(50),
    role_id integer
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- Name: employees_employee_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_employee_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_employee_id_seq OWNER TO postgres;

--
-- Name: employees_employee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_employee_id_seq OWNED BY public.employees.employee_id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    role_id integer NOT NULL,
    role character varying(100),
    description text
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_role_id_seq OWNER TO postgres;

--
-- Name: roles_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_role_id_seq OWNED BY public.roles.role_id;


--
-- Name: skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skills (
    skill_id integer NOT NULL,
    skill character varying(100)
);


ALTER TABLE public.skills OWNER TO postgres;

--
-- Name: skills_skill_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.skills_skill_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.skills_skill_id_seq OWNER TO postgres;

--
-- Name: skills_skill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.skills_skill_id_seq OWNED BY public.skills.skill_id;


--
-- Name: employees employee_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN employee_id SET DEFAULT nextval('public.employees_employee_id_seq'::regclass);


--
-- Name: roles role_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN role_id SET DEFAULT nextval('public.roles_role_id_seq'::regclass);


--
-- Name: skills skill_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills ALTER COLUMN skill_id SET DEFAULT nextval('public.skills_skill_id_seq'::regclass);


--
-- Data for Name: employee_skills; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employee_skills (employee_id, skill_id, proficiency_lvl) FROM stdin;
2	357	PROFESSIONAL
2	360	INTERMEDIATE
2	300	BEGINNER
2	279	INTERMEDIATE
2	377	INTERMEDIATE
2	375	BEGINNER
3	352	PROFESSIONAL
3	297	BEGINNER
3	303	BEGINNER
3	336	PROFESSIONAL
3	308	PROFESSIONAL
3	277	BEGINNER
3	374	PROFESSIONAL
4	265	PROFESSIONAL
4	332	INTERMEDIATE
4	365	BEGINNER
4	275	BEGINNER
4	311	INTERMEDIATE
4	317	BEGINNER
5	294	INTERMEDIATE
5	330	INTERMEDIATE
5	334	BEGINNER
5	369	PROFESSIONAL
5	370	PROFESSIONAL
5	380	BEGINNER
5	349	BEGINNER
1	262	INTERMEDIATE
1	294	PROFESSIONAL
1	328	BEGINNER
1	361	PROFESSIONAL
1	338	BEGINNER
1	309	BEGINNER
1	378	PROFESSIONAL
1	286	PROFESSIONAL
7	321	INTERMEDIATE
7	305	INTERMEDIATE
7	290	INTERMEDIATE
7	292	BEGINNER
8	353	PROFESSIONAL
8	359	INTERMEDIATE
8	263	INTERMEDIATE
8	331	BEGINNER
8	364	BEGINNER
8	379	BEGINNER
9	321	PROFESSIONAL
9	324	PROFESSIONAL
9	327	INTERMEDIATE
9	334	PROFESSIONAL
9	272	BEGINNER
9	274	INTERMEDIATE
9	376	PROFESSIONAL
9	314	INTERMEDIATE
9	381	PROFESSIONAL
10	357	BEGINNER
10	299	INTERMEDIATE
10	302	PROFESSIONAL
10	271	BEGINNER
10	343	BEGINNER
10	285	PROFESSIONAL
11	290	INTERMEDIATE
11	259	INTERMEDIATE
11	356	BEGINNER
11	269	PROFESSIONAL
11	305	INTERMEDIATE
11	306	INTERMEDIATE
11	307	PROFESSIONAL
11	344	PROFESSIONAL
11	377	INTERMEDIATE
12	289	INTERMEDIATE
12	257	BEGINNER
12	324	PROFESSIONAL
12	327	PROFESSIONAL
12	301	INTERMEDIATE
12	334	PROFESSIONAL
12	272	BEGINNER
12	376	BEGINNER
12	314	INTERMEDIATE
12	348	BEGINNER
13	258	BEGINNER
13	260	BEGINNER
13	372	PROFESSIONAL
13	340	INTERMEDIATE
13	276	INTERMEDIATE
13	350	PROFESSIONAL
14	261	INTERMEDIATE
14	358	INTERMEDIATE
14	268	PROFESSIONAL
14	366	PROFESSIONAL
14	312	BEGINNER
14	283	INTERMEDIATE
14	382	INTERMEDIATE
14	355	INTERMEDIATE
14	293	INTERMEDIATE
14	296	INTERMEDIATE
14	304	INTERMEDIATE
14	337	BEGINNER
14	313	BEGINNER
14	346	PROFESSIONAL
16	320	INTERMEDIATE
16	265	PROFESSIONAL
16	332	PROFESSIONAL
16	365	PROFESSIONAL
16	273	BEGINNER
16	275	BEGINNER
16	311	PROFESSIONAL
16	383	INTERMEDIATE
2	267	INTERMEDIATE
2	336	BEGINNER
2	347	PROFESSIONAL
2	284	BEGINNER
2	287	PROFESSIONAL
18	363	PROFESSIONAL
18	268	BEGINNER
18	366	PROFESSIONAL
18	312	PROFESSIONAL
18	286	INTERMEDIATE
18	351	BEGINNER
19	288	BEGINNER
19	384	PROFESSIONAL
19	333	BEGINNER
19	372	INTERMEDIATE
19	341	BEGINNER
19	278	INTERMEDIATE
19	342	INTERMEDIATE
19	319	INTERMEDIATE
3	384	PROFESSIONAL
3	322	BEGINNER
3	326	PROFESSIONAL
3	266	INTERMEDIATE
3	342	INTERMEDIATE
3	345	INTERMEDIATE
3	318	INTERMEDIATE
21	296	PROFESSIONAL
21	337	PROFESSIONAL
21	339	INTERMEDIATE
21	373	INTERMEDIATE
21	316	INTERMEDIATE
22	384	BEGINNER
22	326	INTERMEDIATE
22	280	BEGINNER
22	379	INTERMEDIATE
22	318	BEGINNER
23	290	BEGINNER
23	259	BEGINNER
23	292	PROFESSIONAL
23	269	BEGINNER
23	305	BEGINNER
23	307	PROFESSIONAL
24	261	INTERMEDIATE
24	358	INTERMEDIATE
24	363	BEGINNER
24	268	INTERMEDIATE
24	366	BEGINNER
24	335	BEGINNER
24	312	INTERMEDIATE
24	283	BEGINNER
24	351	BEGINNER
2	258	PROFESSIONAL
2	260	BEGINNER
2	372	INTERMEDIATE
2	276	PROFESSIONAL
2	340	INTERMEDIATE
2	281	BEGINNER
2	350	PROFESSIONAL
26	294	INTERMEDIATE
26	262	PROFESSIONAL
26	361	INTERMEDIATE
26	270	INTERMEDIATE
26	338	BEGINNER
26	378	PROFESSIONAL
26	286	BEGINNER
27	357	INTERMEDIATE
27	360	PROFESSIONAL
27	300	PROFESSIONAL
27	368	INTERMEDIATE
27	375	INTERMEDIATE
27	377	BEGINNER
28	353	BEGINNER
28	331	PROFESSIONAL
28	364	PROFESSIONAL
28	359	BEGINNER
29	281	PROFESSIONAL
29	276	PROFESSIONAL
29	260	BEGINNER
29	350	PROFESSIONAL
30	285	INTERMEDIATE
30	271	PROFESSIONAL
30	367	PROFESSIONAL
30	343	BEGINNER
31	368	INTERMEDIATE
31	300	PROFESSIONAL
31	357	BEGINNER
31	375	INTERMEDIATE
32	257	INTERMEDIATE
32	321	PROFESSIONAL
32	324	BEGINNER
32	327	BEGINNER
32	329	INTERMEDIATE
32	274	PROFESSIONAL
32	306	PROFESSIONAL
32	376	BEGINNER
32	381	PROFESSIONAL
33	321	BEGINNER
33	290	BEGINNER
33	259	BEGINNER
33	356	INTERMEDIATE
33	300	INTERMEDIATE
33	269	BEGINNER
33	305	INTERMEDIATE
33	307	BEGINNER
33	344	INTERMEDIATE
33	377	PROFESSIONAL
34	264	PROFESSIONAL
34	298	BEGINNER
34	267	BEGINNER
34	347	PROFESSIONAL
34	315	INTERMEDIATE
34	284	BEGINNER
34	287	BEGINNER
10	261	INTERMEDIATE
10	268	INTERMEDIATE
10	366	INTERMEDIATE
10	335	BEGINNER
10	312	PROFESSIONAL
10	382	PROFESSIONAL
36	321	INTERMEDIATE
36	290	BEGINNER
36	259	PROFESSIONAL
36	292	PROFESSIONAL
36	305	INTERMEDIATE
36	306	PROFESSIONAL
36	307	BEGINNER
37	294	PROFESSIONAL
37	363	PROFESSIONAL
37	268	PROFESSIONAL
37	312	BEGINNER
37	286	BEGINNER
37	351	PROFESSIONAL
2	321	INTERMEDIATE
2	259	INTERMEDIATE
2	292	BEGINNER
2	269	BEGINNER
2	307	PROFESSIONAL
39	355	PROFESSIONAL
39	323	INTERMEDIATE
39	293	PROFESSIONAL
39	296	BEGINNER
39	314	BEGINNER
39	304	PROFESSIONAL
39	337	PROFESSIONAL
39	313	INTERMEDIATE
39	346	BEGINNER
40	357	INTERMEDIATE
40	300	INTERMEDIATE
40	368	PROFESSIONAL
40	375	PROFESSIONAL
40	279	BEGINNER
41	352	PROFESSIONAL
41	297	INTERMEDIATE
41	336	INTERMEDIATE
41	308	BEGINNER
41	284	INTERMEDIATE
42	294	PROFESSIONAL
42	295	BEGINNER
42	330	PROFESSIONAL
42	334	INTERMEDIATE
42	369	BEGINNER
42	370	INTERMEDIATE
42	338	INTERMEDIATE
42	310	PROFESSIONAL
42	380	PROFESSIONAL
42	349	PROFESSIONAL
31	355	PROFESSIONAL
31	323	INTERMEDIATE
31	293	INTERMEDIATE
31	296	PROFESSIONAL
31	314	BEGINNER
31	337	BEGINNER
31	339	INTERMEDIATE
31	313	BEGINNER
31	346	INTERMEDIATE
44	384	PROFESSIONAL
44	322	PROFESSIONAL
44	326	BEGINNER
44	266	PROFESSIONAL
44	342	BEGINNER
44	345	PROFESSIONAL
45	357	PROFESSIONAL
45	299	PROFESSIONAL
45	302	INTERMEDIATE
45	367	PROFESSIONAL
45	271	BEGINNER
45	343	PROFESSIONAL
45	285	BEGINNER
16	290	INTERMEDIATE
16	259	PROFESSIONAL
16	292	PROFESSIONAL
16	269	BEGINNER
16	306	INTERMEDIATE
16	307	PROFESSIONAL
47	258	INTERMEDIATE
47	276	PROFESSIONAL
47	340	INTERMEDIATE
47	281	INTERMEDIATE
47	350	PROFESSIONAL
48	261	BEGINNER
48	358	PROFESSIONAL
48	363	PROFESSIONAL
48	268	INTERMEDIATE
48	366	INTERMEDIATE
48	335	PROFESSIONAL
48	312	INTERMEDIATE
48	283	PROFESSIONAL
48	382	INTERMEDIATE
49	265	BEGINNER
49	332	INTERMEDIATE
49	365	INTERMEDIATE
49	301	BEGINNER
49	311	PROFESSIONAL
49	317	PROFESSIONAL
50	257	BEGINNER
50	289	PROFESSIONAL
50	324	PROFESSIONAL
50	327	BEGINNER
50	329	BEGINNER
50	272	PROFESSIONAL
50	376	BEGINNER
50	314	INTERMEDIATE
51	353	INTERMEDIATE
51	291	PROFESSIONAL
51	263	INTERMEDIATE
51	331	BEGINNER
51	364	BEGINNER
51	379	BEGINNER
\.


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (employee_id, first_name, last_name, role_id) FROM stdin;
1	Eric	Mason	4
2	John	Holmes	18
3	Carl	Dixon	9
4	Alina	Gray	20
5	Daniel	Russell	1
6	Eric	Mason	10
7	Tony	Bennett	11
8	Melanie	Holmes	8
9	Grace	Ellis	14
10	Amelia	Cameron	7
11	Byron	Mason	3
12	Kate	Warren	12
13	Honey	Brown	17
14	Evelyn	Warren	6
15	Evelyn	Warren	5
16	Roman	Warren	4
17	John	Holmes	16
18	Chester	Perkins	15
19	Abigail	Turner	2
20	Carl	Dixon	21
21	Alberta	Andrews	13
22	Antony	Howard	19
23	Derek	Gray	11
24	Chelsea	Mitchell	6
25	John	Holmes	17
26	Victor	Carroll	10
27	Frederick	Tucker	18
28	Miller	Murray	8
29	Amy	Campbell	17
30	Camila	Chapman	7
31	Maximilian	Hill	18
32	Frederick	Hunt	14
33	Abigail	Moore	3
34	Dale	Farrell	16
35	Amelia	Cameron	6
36	Jessica	Thomas	11
37	Violet	Warren	15
38	John	Holmes	11
39	Roman	Walker	5
40	Wilson	Nelson	18
41	Vanessa	Miller	9
42	Kimberly	Bailey	1
43	Maximilian	Hill	5
44	Naomi	Foster	21
45	Dominik	Miller	7
46	Roman	Warren	11
47	Alissa	Mitchell	17
48	Henry	Perry	6
49	Henry	Morris	4
50	Oliver	Brown	12
51	Lilianna	Johnson	8
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (role_id, role, description) FROM stdin;
1	Database Administrator	Manage and maintain databases, optimize database performance, and ensure data security.
2	Network Engineer	Design, configure, and maintain network infrastructure, troubleshoot connectivity issues, and optimize network performance.
3	Web Developer	Build and maintain websites and web applications, create user-friendly interfaces, and ensure cross-browser compatibility.
4	Systems Administrator	Manage and maintain IT systems, including servers and hardware, ensure system reliability, and provide technical support.
5	DevOps Engineer	Automate and streamline software development and IT operations, implement CI/CD pipelines, and ensure efficient deployments.
6	Machine Learning Engineer	Develop machine learning models, train AI algorithms, and apply data science to solve real-world problems.
7	UI/UX Designer	Create user-friendly interfaces, design wireframes and prototypes, and conduct user research to enhance user experiences.
8	Software Architect	Define software architecture, design system components, and provide technical guidance to development teams.
9	IT Project Manager	Plan and oversee IT projects, manage project teams, and ensure projects are delivered on time and within budget.
10	Data Engineer	Develop data pipelines, manage data storage, and transform data for analytics and reporting.
11	Front-end Developer	Create and optimize the user interface of websites and web applications for an enhanced user experience.
12	Back-end Developer	Build server-side logic and databases, manage application data, and ensure system functionality.
13	Cloud Engineer	Cloud Platforms (e.g., AWS, Azure, Google Cloud), Cloud Deployment, Infrastructure as Code (IaC)
14	Full Stack Developer	Both Front-end and Back-end Development, Web Development Frameworks, Database Management
15	Data Scientist	Analyze and interpret complex data, develop predictive models, and derive actionable insights.
16	Software Tester	Identify software defects, write test cases, and ensure the quality and reliability of software.
17	Cybersecurity Engineer	Implement security measures, detect and mitigate security threats, and secure IT systems.
18	Mobile App Developer	Create mobile applications for various platforms (iOS, Android), and ensure app functionality and performance.
19	Embedded Systems Engineer	Design and develop embedded systems, program microcontrollers, and ensure system functionality.
20	System Administrator	System Administration, Server Management, Network Configuration, Troubleshooting
21	IoT Engineer	Design and develop Internet of Things (IoT) solutions, integrate sensors, and analyze IoT data.
\.


--
-- Data for Name: skills; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.skills (skill_id, skill) FROM stdin;
257	Java
258	Cryptography
259	Responsive Web Design
260	Penetration Testing
261	scikit-learn
262	Hadoop
263	Integration Testing and System Testing
264	Selenium
265	System Administration
266	Sensor Integration
267	pytest
268	Data Manipulation and Cleaning
269	JavaScript
270	Spark
271	Usability Testing
272	Node.js
273	Active Directory
274	Web Development
275	Disaster Recovery Planning
276	Ethical Hacking
277	Scrum
278	TCP/IP
279	iOS Mobile App Development
280	Hardware/Software Integration
281	Malware Analysis
282	Routing and Switching
283	PyTorch
284	Agile Methodologies
285	Sketch
286	Data Engineering
287	Test-Driven Development (TDD)
288	VPN
289	GraphQL
290	HTML
291	Memory Management and Performance Profiling
292	UX/UI Design and Prototyping
293	Docker
294	Data Mining
295	Microsoft SQL Server
296	Kubernetes
297	Kanban
298	JUnit
299	User Centric Design
300	UI Design
301	Security Best Practices
302	Wireframing and Prototyping
303	Technical Documentation
304	SVN
305	Vue.js
306	Angular
307	CSS
308	Budgeting
309	Data Visualization
310	Data Modeling
311	Backup and Recovery
312	Pandas
313	Build Automation
314	Git
315	Manual Testing
316	Cloud Architecture
317	Virtualization Hyper-V
318	Embedded Systems
319	Network Monitoring
320	Troubleshooting
321	React
322	Smart contracts
323	AWS
324	NoSQL
325	Oracle
326	CoAP
327	Django
328	Big Data Technologies
329	Kotlin
330	RDBMS
331	RESTful Architecture
332	Virtualization VMware
333	VoIP (Voice over Internet Protocol)
334	SQL
335	Computer Vision
336	Quality Assurance
337	Azure
338	ETL
339	DevOps
340	Security Auditing
341	Wireless Networking
342	IoT
343	Adobe XD
344	Cross Browser Compatibility
345	Cryptocurrency development
346	Continuous Integration/Continuous Deployment
347	Performance Testing
348	REST
349	MongoDB
350	Intrusion Detection
351	Matplotlib
352	Risk Management
353	System Architecture Design
354	Firewall Configuration
355	GCP
356	Web Accessibility
357	Responsive Design
358	Natural Language Processing
359	Scalability and Performance Optimization
360	Flutter
361	Data Manipulation
362	Blockchain security
363	Machine Learning
364	Software Design Patterns
365	Server Administration
366	AI
367	User Research
368	React Native
369	Cassandra
370	PostgreSQL
371	Incident Response
372	Network Security
373	Cloud Native Application Development
374	Project Planning
375	Android Mobile App Development
376	Flask
377	UX Design
378	Data Warehousing
379	Real-Time Systems
380	MySQL
381	Scala
382	TensorFlow
383	IT Support
384	MQTT
\.


--
-- Name: employees_employee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_employee_id_seq', 51, true);


--
-- Name: roles_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_role_id_seq', 21, true);


--
-- Name: skills_skill_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.skills_skill_id_seq', 384, true);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (employee_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);


--
-- Name: skills skills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (skill_id);


--
-- Name: employee_skills employee_skills_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_skills
    ADD CONSTRAINT employee_skills_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(employee_id);


--
-- Name: employee_skills employee_skills_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_skills
    ADD CONSTRAINT employee_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(skill_id);


--
-- Name: employees employees_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id);


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

