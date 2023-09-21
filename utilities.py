# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 16:06:35 2023

@author: grant and joseph
"""
#importing pandas
import pandas as pd
#importing matplotlib
import matplotlib.pyplot as plt

'''
The section deals with processing the dataset into a dataframe that we can easily analyze it
''' 

#importing data from tech_layoffs.csv as a dataframe
layoffs_df = pd.read_csv('tech_layoffs.csv')

#the 'additonal notes' and 'sources' columns are also unhelpful and will be removed
layoffs_df = layoffs_df.drop(columns=['additional_notes', 'sources'])

#A comma seperated list for each element in the 'industry' column is difficult to work with so we will split each industy into it's own column
#also removed reported date
layoffs_df = pd.concat([layoffs_df[['company', 'total_layoffs', 'impacted_workforce_percentage', 'headquarter_location', 'status' ]], layoffs_df['industry'].str.split(', ', expand=True)], axis=1)

#renaming the columns created
layoffs_df.rename(columns={0: 'industry_1', 1: 'industry_2', 2: 'industry_3'}, inplace=True)

#data analytics, analytics, and data science industries are considered to be the same so we create one uniform name: 'Analytics'
layoffs_df.replace("data analytics", "Analytics", inplace=True)
layoffs_df.replace("Data analytics", "Analytics", inplace=True)
layoffs_df.replace("Data Analytics", "Analytics", inplace=True)
layoffs_df.replace("data Analytics", "Analytics", inplace=True)
layoffs_df.replace("Data science", "Analytics", inplace=True)

#There is a similar situation with Fintech
layoffs_df.replace("FinTech", "Fintech", inplace=True)

#creating our first function that will find the companies with the most layoffs
def mostLayoffs():
    ''' 
    This function will allow the user to see the 10 companies with the most layoffs
    The function will then visulaize that information using a matplotlib bar chart
    '''
    #for simplicity of analysis we are going to remove all companies with 'Unclear' in any field
    #a field being 'Unclear' is essentially null and is not useful for our analysis and needs to be removed
    #additionally we create a seperate dataframe local to this function
    df = layoffs_df
    df = df[df["total_layoffs"].str.contains("Unclear") == False]
    
    #it will also be helpful for analysis to have total layoffs and impacted workforce percentage formated as integers
    df.total_layoffs = df.total_layoffs.astype(int)
    
    #finding the 10 most layoffs by companies, using the sort values function creates a seperate database that we can utlize
    mostLayoffs = df.sort_values('total_layoffs', ascending=False)[:10]
    
    #using the top 10 dataframe to consruct a bar chart in matplotlib
    plot = mostLayoffs.plot(x = "company", y = "total_layoffs", kind = "bar", color = 'lightgreen')
    
    #displaying the bar chart and saving as jpg
    print("This chart shows the top 10 companies with the most layoffs.")
    plt.show()
    
    plot.figure.savefig("Most Layoffs.jpg", bbox_inches = 'tight')
#creating our second function, least layoffs
def leastLayoffs():
    '''
    since we showed user which companies had the most layoffs it only makes sense that we show 
    them the 10 companies with the least layoffs all well. 
    '''
    #for simplicity of analysis we are going to remove all companies with 'Unclear' in any field
    #a field being 'Unclear' is essentially null and is not useful for our analysis and needs to be removed
    #additionally we create a seperate dataframe local to this function
    df = layoffs_df
    df = df[df["total_layoffs"].str.contains("Unclear") == False]
    
    #it will also be helpful for analysis to have total layoffs formated as integers
    df.total_layoffs = df.total_layoffs.astype(int)
    
    #finding the 10 companies with the least layoffs using the sort values function that creates a seperate database we can utilize
    leastLayoffs = df.sort_values('total_layoffs', ascending=True)[:10]
    
    #using the bottom 10 dataframe to consruct a bar chart in matplotlib
    plot = leastLayoffs.plot(x = "company", y = "total_layoffs", kind = "bar", color = 'olive')
    
    #displaying the bar chart and saving as jpg
    print("This chart shows the 10 companies with the least amount of layoffs.")
    plt.show()
    
    plot.figure.savefig("Least Layoffs.jpg", bbox_inches = 'tight')
    
    #some of the private companies on this list are small and irrelevent, here we filter the data further to find just public companies with least layoffs
    public = df.loc[df['status'] == 'Public']
    
    #sorting to show top 10
    pubLeastLayoffs = public.sort_values('total_layoffs', ascending=True)[:10]
    
    #displaying as a bar chart and saving as jpg
    plot2 = pubLeastLayoffs.plot(x = "company", y = "total_layoffs", kind = "bar", color = 'turquoise')
    
    plot2.figure.savefig("Least Layoffs Public.jpg", bbox_inches = 'tight')
    
    
#creating our third function, most common industries
'''
count the number of occurences of each and the display top 10
this is why you removed the unclear removal part and made it exclusive to the function, lots of public companies were unclear
'''
def industries():
    '''
    This function counts the most common industires for layoffs and displays the top 10.
    '''
    #we create a seperate dataframe local to this function
    df = layoffs_df
    
    #gathering the top ten industires from industry 1 column
    result1 = df['industry_1'].value_counts(ascending = False)
    
    #gathering the top ten industries from industry 2 column
    result2 = df['industry_2'].value_counts(ascending = False)
    
    #gathering the top ten industries from industry 3 column
    result3 = df['industry_3'].value_counts(ascending = False)
    
    #joining all series and showing the top ten results
    total = pd.concat([result1, result2, result3])
    total = total.head(10)
    
    #plotting the results
    plot = total.plot(x = "index", y = "0", title = "Most Common Industries for Layoffs", kind = "bar", color = 'tab:purple')
    plt.ylabel("Company Industry")
    
    #displaying the plot and saving as jpg
    print("This bar chart shows the most common industries for layoffs.")
    plt.show()
    
    plot.figure.savefig("Common Industries.jpg", bbox_inches = 'tight')

#creating our fourth function, layoffs between private and public companies 
def PubPriv():
    '''
    This function provides users with the number of layoffs beween publically 
    and privatly held companies
    '''
    #for simplicity of analysis we are going to remove all companies with 'Unclear' in any field
    #a field being 'Unclear' is essentially null and is not useful for our analysis and needs to be removed
    #additionally we create a seperate dataframe local to this function
    df = layoffs_df
    df = df[df["impacted_workforce_percentage"].str.contains("Unclear") == False]
    
    #it will also be helpful for analysis to have total layoffs formated as integers
    df.impacted_workforce_percentage = df.impacted_workforce_percentage.astype(int)
    
    #sorting to just show public companies
    public = df.loc[df['status'] == 'Public']
    
    #totaling layoffs for public companies
    averageLayoffsPublic = round((public['impacted_workforce_percentage'].sum())/ len(public.index))
    
    #sorting to just show private companies
    private = df.loc[df['status'] == 'Private']
    
    #totaling layoffs for private companies
    averageLayoffsPrivate = round((private['impacted_workforce_percentage'].sum())/ len(private.index))
    
    #designing the plot
    fig = plt.figure()
    plot = fig.add_axes([0,0,1,1])
    plot.bar(['Public Companies', 'Private Companies'], [averageLayoffsPublic, averageLayoffsPrivate], color = 'cyan')
    plot.set_title("Layoffs Between Public and Privately Traded Companies")
    plt.ylabel("Average Percentage Laid Off")
    
    #diplaying the pie chart and saving as jpg
    print("This bar chart shows the percentage of layoffs between publicly\n and privately held companies.")
    plt.show()
    
    fig.savefig("Public v. Private.jpg", bbox_inches = 'tight')
    
#grouping all functions into one main
def main():
    mostLayoffs()
    leastLayoffs()
    industries()
    PubPriv()
    

if __name__ == "__main__":
    main()

    
    
    