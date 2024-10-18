# IDS706_complex_sql_hx84
![CI](https://github.com/nogibjj/IDS706_package_python_CLI/actions/workflows/CICD.yml/badge.svg)

# Overview

You can find this tool [here](https://pypi.org/project/complex-sql-tool/1.0.1/)

## Objective

Implement an ETL (Extract, Transform, Load) process for the Adult dataset, split it into multiple relational tables, and perform complex SQL queries involving joins, aggregations, and sorting.

## Tasks

* Extract: Download the Adult dataset.
* Transform & Load: Clean the data, split it into multiple tables, and load it into a AWS based MySQL database.
* Queries: Write complex SQL queries involving joins, aggregations, and sorting.

## Structure

```bash
.
├── img
│   ├── database.png
│   └── test.png
├── LICENSE
├── main.py
├── Makefile
├── mylib
│   ├── extract.py
│   ├── __init__.py
│   ├── query.py
│   └── transform_load.py
├── README.md
├── requirements.txt
├── sql
│   ├── create_tables.sql
│   ├── query1.sql
│   └── query2.sql
└── test_main.py
```

# Installation

To install the Complex SQL Tool, use `pip`:

```bash
pip install complex_sql_tool
```

# Usage
After installing, you can use the tool with the following command:

```bash
complex_sql_tool --help
```

## Examples

```bash
complex_sql_tool extract
complex_sql_tool load
complex_sql_tool query
```

# SQL query

## Create Table

* Defines three tables: personal_info, employment_info, and income_info.
* Each table has an id column as the primary key with AUTO_INCREMENT.
* The tables store different aspects of the data for normalization.

```SQL
DROP TABLE IF EXISTS personal_info;
DROP TABLE IF EXISTS employment_info;
DROP TABLE IF EXISTS income_info;

CREATE TABLE personal_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    age INT,
    sex VARCHAR(10),
    race VARCHAR(50),
    native_country VARCHAR(50),
    marital_status VARCHAR(50),
    relationship VARCHAR(50)
);

CREATE TABLE employment_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    workclass VARCHAR(50),
    occupation VARCHAR(50),
    education VARCHAR(50),
    education_num INT,
    hours_per_week INT,
    capital_gain INT,
    capital_loss INT,
    fnlwgt INT
);

CREATE TABLE income_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    income VARCHAR(20)
);
```

## Query1

* For each sex and education level (with more than 50 individuals), calculate the average age and average hours per week, sorted by average hours per week in descending order.

```SQL
SELECT
    p.sex,
    e.education,
    AVG(p.age) AS average_age,
    AVG(e.hours_per_week) AS average_hours_per_week,
    COUNT(*) AS count
FROM
    personal_info p
JOIN
    employment_info e ON p.id = e.id
GROUP BY
    p.sex, e.education
HAVING
    COUNT(*) > 50
ORDER BY
    average_hours_per_week DESC;
```

## Query2
* For each native country (with more than 50 individuals), calculate the number of people, number of high-income individuals, and the percentage of high-income individuals, sorted by high-income percentage in descending order.
```SQL
SELECT
    p.native_country,
    COUNT(*) AS total_people,
    SUM(CASE WHEN i.income = '>50K' THEN 1 ELSE 0 END) AS high_income_people,
    ROUND(SUM(CASE WHEN i.income = '>50K' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS high_income_percentage
FROM
    personal_info p
JOIN
    income_info i ON p.id = i.id
GROUP BY
    p.native_country
HAVING
    COUNT(*) > 50
ORDER BY
    high_income_percentage DESC;
```

# Results

## Database in MYSQL

![image1](https://github.com/nogibjj/IDS706_package_python_CLI/img/database.png)

## Query Results

### query1

| sex    | education    | average_age | average_hours_per_week | count |
|--------|--------------|-------------|------------------------|-------|
| Male   | Prof-school  | 45.6116     | 47.9256                | 484   |
| Female | Doctorate    | 45.3256     | 47.3023                | 86    |
| Male   | Doctorate    | 48.3272     | 46.8869                | 327   |
| Male   | Masters      | 44.4903     | 45.0657                | 1187  |
| Female | Prof-school  | 40.1957     | 44.7935                | 92    |
| Male   | Bachelors    | 40.3217     | 44.0375                | 3736  |
| Male   | Assoc-voc    | 38.9399     | 43.7540                | 882   |
| Male   | Assoc-acdm   | 38.0464     | 42.5542                | 646   |
| Male   | HS-grad      | 39.1157     | 42.4814                | 7111  |
| Male   | Some-college | 37.0174     | 41.5284                | 4485  |
| Female | Masters      | 43.0746     | 41.1138                | 536   |
| Male   | 1st-4th      | 45.2459     | 40.6230                | 122   |
| Male   | 7th-8th      | 48.0350     | 40.4095                | 486   |
| Male   | 5th-6th      | 42.3855     | 39.8594                | 249   |
| Male   | 9th          | 40.6432     | 39.6514                | 370   |
| Male   | 10th         | 38.3464     | 39.3370                | 638   |
| Female | Bachelors    | 35.6356     | 39.3292                | 1619  |
| Female | Assoc-voc    | 37.8720     | 37.8300                | 500   |
| Male   | 12th         | 33.1176     | 37.7682                | 289   |
| Female | Assoc-acdm   | 36.3610     | 37.3587                | 421   |
| Female | HS-grad      | 38.6782     | 36.5773                | 3390  |
| Male   | 11th         | 33.4078     | 36.3122                | 743   |
| Female | 7th-8th      | 49.6938     | 36.2000                | 160   |
| Female | 5th-6th      | 44.3690     | 36.0476                | 84    |
| Female | Some-college | 33.7406     | 34.5748                | 2806  |
| Female | 9th          | 42.1319     | 33.9167                | 144   |
| Female | 10th         | 35.4475     | 32.1119                | 295   |
| Female | 12th         | 29.7569     | 31.7917                | 144   |
| Female | 11th         | 30.5463     | 29.8218                | 432   |

---

### query2

| native_country     | total_people | high_income_people | high_income_percentage |
|--------------------|--------------|--------------------|------------------------|
| India              | 100          | 40                 | 40.00                  |
| Taiwan             | 51           | 20                 | 39.22                  |
| Japan              | 62           | 24                 | 38.71                  |
| Italy              | 73           | 25                 | 34.25                  |
| England            | 90           | 30                 | 33.33                  |
| Canada             | 121          | 39                 | 32.23                  |
| Germany            | 137          | 44                 | 32.12                  |
| Philippines        | 198          | 61                 | 30.81                  |
| China              | 75           | 20                 | 26.67                  |
| Cuba               | 95           | 25                 | 26.32                  |
| Total              | 583          | 146                | 25.04                  |
| United-States      | 29170        | 7171               | 24.58                  |
| South              | 80           | 16                 | 20.00                  |
| Poland             | 60           | 12                 | 20.00                  |
| Jamaica            | 81           | 10                 | 12.35                  |
| Puerto-Rico        | 114          | 12                 | 10.53                  |
| El-Salvador        | 106          | 9                  | 8.49                   |
| Vietnam            | 67           | 5                  | 7.46                   |
| Mexico             | 643          | 33                 | 5.13                   |
| Guatemala          | 64           | 3                  | 4.69                   |
| Columbia           | 59           | 2                  | 3.39                   |
| Dominican-Republic | 70           | 2                  | 2.86                   |

---

## Test

![image2](https://github.com/nogibjj/IDS706_package_python_CLI/img/test.png)