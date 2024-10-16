# Standardized Time and Calendar System
The Standardized Time and Calendar System (STCS) is a system which replaces the traditional time and calendar systems to make them more intuitive and decimalized.

## Time
### Definition
The STCS defines time in the following format:

- Each day is separated into 10 hours
- Each hour is separated into 100 minutes
- Each hour is separated into 100 seconds

### Conversion
The conversion from traditional units to STCS units (known as standardized units) is as follows:

| Standardized Unit | Equivalent Traditional Unit |
|:-----------------:|:---------------------------:|
| 1s                | 0.864 s                     |
| 1 min             | 1.44 mins                   |
| 1 hr              | 2.4 hrs                     |
| 1 day             | 1 day                       |

## Calendar
### Definition
The STCS defines the calendar in the following format:

- Each year is divided into 12 months with 30 days in each month
- An extra 5 days is added at the end of the year as an interannual period
- A leap year occurs whenever the year is divisible by 4 or 400 but not by 100
- During a leap year, the interannual period is extended to 6 days
- Each month is divided into 3 weeks, each lasting 10 days
- The year 1 is defined as the traditional year 2000. For example, the traditional year 2025 is year 25 in STCS format

## CLI
### `conv` Command
The `conv` command converts between STCS and traditional times and dates.

#### Time
##### Usage
stcs conv time [OPTION] [TIMESTAMP]

##### Flags
- `--from-stdz`: Converts the timestamp from STCS format to traditional format
- `--from-traditional`: Converts the timestamp from traditional format to STCS format

##### Example
```cmd
$ stcs conv time --from-stdz 5:86:21
14:04:08
```

#### Date
##### Usage
stcs conv date [OPTION] [DATESTAMP]

##### Flags
- `--from-stdz`: Converts the datestamp from STCS format to traditional format
- `--from-traditional`: Converts the datestamp from traditional format to STCS format

##### Example
```cmd
$ stcs conv date --from-stdz 08/02/24
07/02/2024
```

### `date` Command
Returns the current date in STCS format

#### Example
```cmd
$ stcs date
19/10/24 STDZ
```
**NOTE: The `STDZ` after the date denotes that the date is in STCS format. You will see this after every standardized time or date.**

### `time` Command
Returns the current time in STCS format

#### Example
```cmd
$ stcs time
09:13:96 STDZ
```

### `now` Command
Returns the current time and date in STCS format

#### Example
```cmd
$ stcs now
19/10/24 09:14:34 STDZ
```
