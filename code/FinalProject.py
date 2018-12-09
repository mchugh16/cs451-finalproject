
# Julia Jaschke and Mira Chugh
# Final Project
# Some cleaning of data adapted from Kaggle Kernel

import numpy as np
import fiona
import geopandas as gpd
from geopandas.tools import sjoin
from matplotlib import pyplot as plt
import pandas as pd
from shapely.geometry import Point
import os
import csv





def main():
    """Main Program"""



    clusterlist = headers("data-science-for-good/Dept_37-00027/Clusters_noLoc.csv")

    filename_Rins = "data-science-for-good/Dept_37-00027/Clusters_noLoc.csv"

    DictRins = makeClusterDict(clusterlist, filename_Rins)
    Dept37(DictRins)





def makeClusterDict(clusterlist , filename):
        dict = {}
        for i in clusterlist:
            dict[i] = makeDict2(filename , i)
        dictRINS = {}


        #cluster number is the key , rins are value
        for cluster_num, rin_list in dict.items():
            for rin in rin_list:
                dictRINS[rin] = int(cluster_num)

        return(dictRINS)

def returnDFS(police_arrest_df, dictionary):
    cluster0_df = pd.DataFrame()
    cluster1_df = pd.DataFrame()
    cluster2_df = pd.DataFrame()
    #cluster3_df = pd.DataFrame()
    #cluster4_df = pd.DataFrame()
    toReturn = []
    #print(dictionary)

    for index, row in police_arrest_df.iterrows():

        if dictionary[str(int(row['RIN']))] == 0:
            cluster0_df = cluster0_df.append(row)
        elif dictionary[str(int(row['RIN']))] == 1:
            cluster1_df = cluster1_df.append(row)
        elif dictionary[str(int(row['RIN']))] == 2:
            cluster2_df = cluster2_df.append(row)
        # elif dictionary[str(int(row['RIN']))] == 3:
        #     cluster3_df = cluster3_df.append(row)
        # elif dictionary[str(int(row['RIN']))] == 4:
        #     cluster4_df = cluster4_df.append(row)
    toReturn.append(cluster0_df)
    toReturn.append(cluster1_df)
    toReturn.append(cluster2_df)
    # toReturn.append(cluster3_df)
    # toReturn.append(cluster4_df)
    return toReturn


def returnRINS(police_arrest_df):
    rins = []
    for index, row in police_arrest_df.iterrows():
        rins.append(row['RIN'])
    print(rins)
    
def Dept37(RINdictionary ):
    dept_of_interest = "Dept_37-00027"
    dept_folder = "./data-science-for-good/" + dept_of_interest + "/"

    #census_data_folder, police_shp_folder, police_csv = os.listdir(dept_folder)

    files = list(os.listdir(dept_folder))

    #os.listdir - returns a list of containing the names of the entries in the directories given path
    for file in files:
        if "Shapefiles" in file:
            police_shp_folder = file

        #Prepped csv file
        if "EstLatLong" in file:
            other_csv = file

        if "ACS" in file:
            census_data_folder = file
        if "tract" in file:
            census_tract = file


    for file in os.listdir(dept_folder+police_shp_folder+"/"):      # look at police data
        if ".shp" in file:
            shp_file = file

    police_shp_gdf = gpd.read_file(dept_folder+police_shp_folder+'/'+shp_file)

    #police_arrest_df = pd.read_csv(dept_folder+police_csv).iloc[1:].reset_index(drop=True)

    #TRIAL
    police_arrest_df = pd.read_csv(dept_folder+other_csv).iloc[1:].reset_index(drop=True)


    #police_arrent_df includes the RIN which we want to use to use to

    ##CREATE A FUNCTION HERE THAT GOES THROUGH POLICE ARREST DF THAT RETURNS 4 other dfs


    #drop rows without latitude/longitude

    latlon_exists_index = police_arrest_df[['LOCATION_LATITUDE','LOCATION_LONGITUDE']].dropna().index

    police_arrest_df= police_arrest_df.iloc[latlon_exists_index].reset_index(drop=True)
    police_arrest_df['LOCATION_LATITUDE'] = (police_arrest_df['LOCATION_LATITUDE']
                                         .astype('float'))
    police_arrest_df['LOCATION_LONGITUDE'] = (police_arrest_df['LOCATION_LONGITUDE']
                                         .astype('float'))



    DFList = returnDFS(police_arrest_df, RINdictionary)
    print(DFList)
    Cluster0_df = DFList[0]
    Cluster1_df = DFList[1]
    Cluster2_df = DFList[2]
    # Cluster3_df = DFList[3]
    # Cluster4_df = DFList[4]



    #check if lat,long or long,lat
    police_arrest_df['geometry'] = (police_arrest_df
                                .apply(lambda x: Point(x['LOCATION_LONGITUDE'],
                                                       x['LOCATION_LATITUDE']),
                                       axis=1))


    Cluster0_df['geometry'] = (Cluster0_df
                                .apply(lambda x: Point(x['LOCATION_LONGITUDE'],
                                                       x['LOCATION_LATITUDE']),
                                       axis=1))

    Cluster1_df['geometry'] = (Cluster1_df
                                .apply(lambda x: Point(x['LOCATION_LONGITUDE'],
                                                       x['LOCATION_LATITUDE']),
                                       axis=1))

    Cluster2_df['geometry'] = (Cluster2_df
                                .apply(lambda x: Point(x['LOCATION_LONGITUDE'],
                                                       x['LOCATION_LATITUDE']),
                                       axis=1))

    # Cluster3_df['geometry'] = (Cluster3_df
    #                             .apply(lambda x: Point(x['LOCATION_LONGITUDE'],
    #                                                    x['LOCATION_LATITUDE']),
    #                                    axis=1))
    #
    # Cluster4_df['geometry'] = (Cluster4_df
    #                             .apply(lambda x: Point(x['LOCATION_LONGITUDE'],
    #                                                    x['LOCATION_LATITUDE']),
    #                                    axis=1))
    #



    police_arrest_gdf = gpd.GeoDataFrame(police_arrest_df, geometry='geometry')
    Cluster0_gdf = gpd.GeoDataFrame(Cluster0_df, geometry='geometry')
    Cluster1_gdf = gpd.GeoDataFrame(Cluster1_df, geometry='geometry')
    Cluster2_gdf = gpd.GeoDataFrame(Cluster2_df, geometry='geometry')
    # Cluster3_gdf = gpd.GeoDataFrame(Cluster3_df, geometry='geometry')
    # Cluster4_gdf = gpd.GeoDataFrame(Cluster4_df, geometry='geometry')
    #

    police_arrest_gdf.crs = {'init' :'epsg:4326'}
    Cluster0_gdf.crs = {'init' :'epsg:4326'}
    Cluster1_gdf.crs = {'init' :'epsg:4326'}
    Cluster2_gdf.crs = {'init' :'epsg:4326'}
    # Cluster3_gdf.crs = {'init' :'epsg:4326'}
    # Cluster4_gdf.crs = {'init' :'epsg:4326'}



    #merge with shapefiles

    police_shp_gdf.crs = {'init' :'esri:102739'}
    police_shp_gdf = police_shp_gdf.to_crs(epsg='4326')


    #print("police shape file: ")
    #print(police_shp_gdf.head())

    #print("police arrest data: ")
    #print(police_arrest_gdf.head(3))

    #visualize

    fig1,ax1 = plt.subplots()
    police_shp_gdf.plot(ax=ax1,column='SECTOR')
    #for point in police_arrest_gdf:
        # point is the value and we want to assign it a color based on its key in the dictionary of clusters(so based on cluster)

    police_arrest_gdf.plot(ax=ax1,marker='.',color='k',markersize=4)  #plotting the police arrest data
    Cluster0_gdf.plot(ax=ax1,marker='.',color='g',markersize=5)
    Cluster1_gdf.plot(ax=ax1,marker='.',color='r',markersize=5)
    Cluster2_gdf.plot(ax=ax1,marker='.',color='purple',markersize=5)
    # Cluster3_gdf.plot(ax=ax1,marker='.',color='white',markersize=5)
    # Cluster4_gdf.plot(ax=ax1,marker='.',color='orange',markersize=5)

    fig1.set_size_inches(7,7)



    ######## Now back to census data

    #look at poverty

    for folder in os.listdir(dept_folder+census_data_folder):
        if 'poverty' in folder:
            poverty_folder = folder


    #poverty_acs_file_meta, poverty_acs_file_ann = os.listdir(dept_folder+
                                                   #census_data_folder+'/'+
                                                  # poverty_folder)

    povertyFiles = list(os.listdir(dept_folder+census_data_folder+'/'+poverty_folder))

    #unpack poverty files
    for file in povertyFiles:
        if "meta" in file:
            poverty_acs_file_meta = file
        if "ann" in file:
            poverty_acs_file_ann = file


    census_poverty_df = pd.read_csv(dept_folder+census_data_folder+'/'+poverty_folder+'/'+poverty_acs_file_ann)

    census_poverty_df = census_poverty_df.iloc[1:].reset_index(drop=True)

    # Rename Census Tract ID column in ACS Poverty CSV to align with Census Tract Shapefile
    census_poverty_df = census_poverty_df.rename(columns={'GEO.id2':'GEOID'})


    census_tracts_gdf = gpd.read_file(dept_folder+census_tract+'/'+"cb_2017_48_tract_500k.shp")

    #Merge Census Tract GeoDataFrame (from Shapefile) with ACS Poverty DataFrame
    # using the 'GEOID', or Census Tract 11-digit numerical ID.
    census_merged_gdf = census_tracts_gdf.merge(census_poverty_df, on = 'GEOID')

    #Make sure everything is using EPSG:4326
    census_merged_gdf = census_merged_gdf.to_crs(epsg='4326')

    # #overlay census tract map

    fig2,ax2 = plt.subplots()
    police_shp_gdf.plot(ax=ax2,column='SECTOR')
    police_arrest_gdf.plot(ax=ax2,marker='.',color='k',markersize=5)
    Cluster0_gdf.plot(ax=ax2,marker='.',color='g',markersize=5)
    Cluster1_gdf.plot(ax=ax2,marker='.',color='r',markersize=5)
    Cluster2_gdf.plot(ax=ax2,marker='.',color='purple',markersize=5)
    # Cluster3_gdf.plot(ax=ax2,marker='.',color='white',markersize=5)
    # Cluster4_gdf.plot(ax=ax2,marker='.',color='orange',markersize=5)
    census_merged_gdf.plot(ax=ax2,color='#74b9ff',alpha=.4,edgecolor='white')
    fig2.set_size_inches(10,10)




    # now, look further into the map

    # Check which arrest Points lie within the first Police District
    test_join = sjoin(police_arrest_gdf,police_shp_gdf.iloc[0:1])

    fig3,ax3 = plt.subplots()
    police_shp_gdf.iloc[0:1].plot(ax=ax3)
    Cluster0_gdf.plot(ax=ax3,marker='.',color='g',markersize=5)
    Cluster1_gdf.plot(ax=ax3,marker='.',color='r',markersize=5)
    Cluster2_gdf.plot(ax=ax3,marker='.',color='purple',markersize=5)
    # Cluster3_gdf.plot(ax=ax3,marker='.',color='white',markersize=5)
    # Cluster4_gdf.plot(ax=ax3,marker='.',color='orange',markersize=5)
    test_join.plot(ax=ax3,marker='o',color='k',markersize=10)
    fig3.set_size_inches(7,7)

    plt.show()

def headers(filename):
    headers = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)                                            # read csv file
        headers = (next(reader))
    return headers


def makeDict2(file , cluster):
    clusterNum = []
    with open(file) as csvfile:
        df = pd.read_csv(csvfile)
        saved_column = df[cluster]
        for item in saved_column:
            if item != "stop":
                clusterNum.append(item)
            else:
                break

    return clusterNum




#The functions below were used to change the CSV file into numerical values from
#string values in order to run our clustering algorithm
def ChangeGender(file):
    file_handler = open(file, "r")
    data = pd.read_csv(file_handler, sep = ",")
    gender = {'M': 1,'F': 2 , 'U' : 3 }

    row = 0

    for item in data.SUBJECT_GENDER:

        if item == "stop":
            break
        else:
             item = gender[item]
             data.set_value(row, "SUBJECT_GENDER", item)
             row+=1

    data.to_csv(file, index=False)


def ChangeRace(file):
    file_handler = open(file, "r")
    data = pd.read_csv(file_handler, sep = ",")
    gender = {'Asian': 1,'Black': 2 , 'Unknown' : 3 , 'Hispanic' : 4, 'White' : 5}

    row = 0

    for item in data.SUBJECT_RACE:

        if item == "stop":
            break
        else:
             item = gender[item]
             data.set_value(row, "SUBJECT_RACE", item)
             row+=1

    data.to_csv(file, index=False)


def ChangeDistrict(file):
    file_handler = open(file, "r")
    data = pd.read_csv(file_handler, sep = ",")
    gender = {'AD': 1,'AP': 2 , 'BA' : 3 , 'CH' : 4, 'DA' : 5 , 'ED' : 6, 'FR' : 7 , 'GE' : 8 , 'HE': 9 , 'ID' : 10 , 'U' : 11 , '88' : 12}

    row = 0

    for item in data.LOCATION_DISTRICT:

        if item == "stop":
            break
        else:
             item = gender[item]
             data.set_value(row, "LOCATION_DISTRICT", item)
             row+=1

    data.to_csv(file, index=False)

def IncidentReason(file):
    file_handler = open(file, "r")
    data = pd.read_csv(file_handler, sep = ",")

    categories = data.INCIDENT_REASON.unique()
    dict = {}
    for i in range(len(categories)):
        if categories[i] == 'stop':
            break
        dict[categories[i]] = i
    row = 0

    for item in data.INCIDENT_REASON:
        if item == "stop":
            break
        else:
             item = dict[item]
             data.set_value(row, "INCIDENT_REASON", item)
             row+=1

    data.to_csv(file, index=False)


def ReasonForForce(file):
    file_handler = open(file, "r")
    data = pd.read_csv(file_handler, sep = ",")

    categories = data.REASON_FOR_FORCE.unique()
    dict = {}
    for i in range(len(categories)):
        if categories[i] == 'stop':
            break
        dict[categories[i]] = i
    row = 0

    for item in data.REASON_FOR_FORCE:
        if item == "stop":
            break
        else:
             item = dict[item]
             data.set_value(row, "REASON_FOR_FORCE", item)
             row+=1
    data.to_csv(file, index=False)

def Subject_Role(file):
    file_handler = open(file, "r")
    data = pd.read_csv(file_handler, sep = ",")

    categories = data.SUBJECT_ROLE.unique()

    dict = {}
    for i in range(len(categories)):
        if categories[i] == 'stop':
            break
        dict[categories[i]] = i
    row = 0

    for item in data.SUBJECT_ROLE:

        if item == "stop":
            break
        else:
             item = dict[item]
             data.set_value(row, "SUBJECT_ROLE", item)
             row+=1

    data.to_csv(file, index=False)

def SUBJECT_INJURY_TYPE(file):
    file_handler = open(file, "r")
    data = pd.read_csv(file_handler, sep = ",")

    categories = data.SUBJECT_INJURY_TYPE.unique()

    dict = {}
    for i in range(len(categories)):
        if categories[i] == 'stop':
            break
        dict[categories[i]] = i
    row = 0
    for item in data.SUBJECT_INJURY_TYPE:
        if item == "stop":
            break
        else:
             item = dict[item]
             data.set_value(row, "SUBJECT_INJURY_TYPE", item)
             row+=1
    data.to_csv(file, index=False)

def OFFICER_INJURY_TYPE(file):
    file_handler = open(file, "r")
    data = pd.read_csv(file_handler, sep = ",")

    categories = data.OFFICER_INJURY_TYPE.unique()

    dict = {}
    for i in range(len(categories)):
        if categories[i] == 'stop':
            break
        dict[categories[i]] = i
    row = 0
    for item in data.OFFICER_INJURY_TYPE:
        if item == "stop":
            break
        else:
             item = dict[item]
             data.set_value(row, "OFFICER_INJURY_TYPE", item)
             row+=1
    data.to_csv(file, index=False)


def Street_name(file):
    file_handler = open(file, "r")
    data = pd.read_csv(file_handler, sep = ",")

    categories = data.LOCATION_FULL_STREET_ADDRESS_OR_INTERSECTION.unique()

    dict = {}
    for i in range(len(categories)):
        if categories[i] == 'stop':
            break
        dict[categories[i]] = i
    row = 0

    for item in data.LOCATION_FULL_STREET_ADDRESS_OR_INTERSECTION:
        if item == "stop":
            break
        else:
             item = dict[item]
             data.set_value(row, "LOCATION_FULL_STREET_ADDRESS_OR_INTERSECTION", item)
             row+=1
    data.to_csv(file, index=False)



def Type_force(file):

    file_handler = open(file, "r")
    data = pd.read_csv(file_handler, sep = ",")

    categories = data.TYPE_OF_FORCE_USED4.unique()

    dict = {}
    for i in range(len(categories)):
        if categories[i] == 'stop':
            break
        dict[categories[i]] = i
        row = 0
    for item in data.TYPE_OF_FORCE_USED4:

        if item == "stop":
            break
        else:
             item = dict[item]
             data.set_value(row, "TYPE_OF_FORCE_USED4", item)
             row+=1

    data.to_csv(file, index=False)


def REASON_FOR_FORCE1(file):

    file_handler = open(file, "r")
    data = pd.read_csv(file_handler, sep = ",")

    categories = data.REASON_FOR_FORCE1.unique()

    dict = {}
    for i in range(len(categories)):
        if categories[i] == 'stop':
            break
            dict[categories[i]] = i
    row = 0

    for item in data.REASON_FOR_FORCE1:
        if item == "stop":
            break
        else:
             item = dict[item]
             data.set_value(row, "REASON_FOR_FORCE1", item)
             row+=1

    data.to_csv(file, index=False)

def SUBJECT_DESCRIPTION(file):
    file_handler = open(file, "r")
    data = pd.read_csv(file_handler, sep = ",")

    categories = data.SUBJECT_DESCRIPTION.unique()

    dict = {}
    for i in range(len(categories)):
        if categories[i] == 'stop':
            break
        dict[categories[i]] = i
    row = 0
    for item in data.SUBJECT_DESCRIPTION:

        if item == "stop":
            break
        else:
             item = dict[item]
             data.set_value(row, "SUBJECT_DESCRIPTION", item)
             row+=1

    data.to_csv(file, index=False)


if __name__ == '__main__':
        main()
