
#Julia Jaschke and Mira Chugh
#Final Project

import numpy as np
import fiona
import geopandas as gpd
from geopandas.tools import sjoin
#from geopandas import GeoSeries, GeoDataFrame
from matplotlib import pyplot as plt
import pandas as pd
from shapely.geometry import Point
import os




def main():
    """Main Program"""
    Dept37()




def Dept37():
    dept_of_interest = "Dept_37-00027"
    dept_folder = "./data-science-for-good/" + dept_of_interest + "/"

    #census_data_folder, police_shp_folder, police_csv = os.listdir(dept_folder)

    files = list(os.listdir(dept_folder))

    #os.listdir - returns a list of containing the names of the entries in the directories given path
    for file in files:
        if "Shapefiles" in file:
            police_shp_folder = file
        if "prepped" in file:
            police_csv = file
        if "ACS" in file:
            census_data_folder = file
        if "tract" in file:
            census_tract = file


    for file in os.listdir(dept_folder+police_shp_folder+"/"):      # look at police data
        if ".shp" in file:
            shp_file = file

    police_shp_gdf = gpd.read_file(dept_folder+police_shp_folder+'/'+shp_file)

    police_arrest_df = pd.read_csv(dept_folder+police_csv).iloc[1:].reset_index(drop=True)

    #print(police_shp_gdf.head(3))                          #show data

    #drop rows without latitude/longitude

    latlon_exists_index = police_arrest_df[['LOCATION_LATITUDE','LOCATION_LONGITUDE']].dropna().index

    police_arrest_df = police_arrest_df.iloc[latlon_exists_index].reset_index(drop=True)
    police_arrest_df['LOCATION_LATITUDE'] = (police_arrest_df['LOCATION_LATITUDE']
                                         .astype('float'))
    police_arrest_df['LOCATION_LONGITUDE'] = (police_arrest_df['LOCATION_LONGITUDE']
                                         .astype('float'))

    ###want to conver lat/long into points

    #check is lat,long or long,lat
    police_arrest_df['geometry'] = (police_arrest_df
                                .apply(lambda x: Point(x['LOCATION_LONGITUDE'],
                                                       x['LOCATION_LATITUDE']),
                                       axis=1))

    police_arrest_gdf = gpd.GeoDataFrame(police_arrest_df, geometry='geometry')
    police_arrest_gdf.crs = {'init' :'epsg:4326'}


    #merge with shapefiles

    police_shp_gdf.crs = {'init' :'esri:102739'}
    police_shp_gdf = police_shp_gdf.to_crs(epsg='4326')

    #print("police shape file: ")
    #print(police_shp_gdf.head())

    #print("police arrest data: ")
    #print(police_arrest_gdf.head())

    #visualize

    fig1,ax1 = plt.subplots()
    police_shp_gdf.plot(ax=ax1,column='SECTOR')
    police_arrest_gdf.plot(ax=ax1,marker='.',color='k',markersize=4)
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
    census_merged_gdf.plot(ax=ax2,color='#74b9ff',alpha=.4,edgecolor='white')
    fig2.set_size_inches(10,10)




    # now, look further into the map

    # Check which arrest Points lie within the first Police District
    test_join = sjoin(police_arrest_gdf,police_shp_gdf.iloc[0:1])

    fig3,ax3 = plt.subplots()
    police_shp_gdf.iloc[0:1].plot(ax=ax3)
    test_join.plot(ax=ax3,marker='o',color='k',markersize=10)
    fig3.set_size_inches(7,7)

    plt.show()



if __name__ == '__main__':
        main()
