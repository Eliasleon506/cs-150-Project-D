#  Deforestation: Not an Agricultural Issue 
- **Course**: CS-150 – *Community Action Computing*
- **Author**: Elias Leon


This project is a satirical exploration of **how data visualization can be manipulated to mislead audiences**. Using real-world data on **forest land** and **agricultural land** percentages, this Dash web app makes the argument: that agriculture is not responsible for deforestation.

By selectively filtering and framing the data—specifically by omitting years before major environmental policy changes—we craft a narrative that hides long-term correlations between agriculture and forest loss.


## The Strategy for misleading 

1. **Data Selection**:  
   The dataset starts **after 1991**, conveniently excluding earlier decades where deforestation and agricultural expansion showed clearer correlation.

2. **Visual Framing**:  
   Clean, modern visuals (line and pie charts) give a false sense of neutrality and authority.
3. **Interactivity**: 
   Country and year selectors make the app feel dynamic and customizable—giving the user control.

---

##  Data Sources

- **Forest Land**: World Bank – *Forest area (% of land area)*  
  - Key columns: country,  Forest area (% of land area) per year column 

- **Agricultural Land**: World Bank – *Agricultural land (% of land area)*  
  - Key columns: country,  Agricultural land (% of land area) per year column 
- Both datasets are publicly available and were imported from CSV files.
- Both datasets are merged in the application for easier us by adding a year column 
---



