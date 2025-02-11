# Import necessary libraries

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# standard libraries
from time import time
# custom functions
try:
    from packages.common import requestAndParse
except ModuleNotFoundError:
    from common import requestAndParse


# extracts desired data from listing banner
def extract_listingBanner(listing_soup, requested_url):
    listing_bannerGroup_valid = False

    try:
        listing_bannerGroup = listing_soup.find("div", class_="css-ur1szg e11nt52q0")
        listing_bannerGroup_valid = True
    except:
        print("[ERROR] Error occurred in function extract_listingBanner")
        companyName = "NA"
        company_starRating = "NA"
        company_offeredRole = "NA"
        company_roleLocation = "NA"

        

    if listing_bannerGroup_valid:
        try:
            company_starRating = listing_bannerGroup.find("span", class_="css-1pmc6te e11nt52q4").getText()
        except:
            company_starRating = "NA"
        if company_starRating != "NA":
            try:
                #companyName = listing_bannerGroup.find("div", class_="css-16nw49e e11nt52q1").getText().replace(company_starRating,'')
                companyName = listing_bannerGroup.find("div", class_="d-flex").getText().replace(company_starRating,'')
            except:
                companyName = "NA"
                #css-87uc0g e1tk4kwz1
            # company_starRating.replace("★", "")
            company_starRating = company_starRating[:-1]
        else:
            try:
                companyName = listing_bannerGroup.find("div", class_="css-16nw49e e11nt52q1").find("div", class_="d-flex").getText()

                #css-16nw49e e11nt52q1
            except:
                companyName = "NA"

        try:
            company_offeredRole = listing_bannerGroup.find("div", class_="css-17x2pwl e11nt52q6").getText()
        except:
            company_offeredRole = "NA"

        try:
            company_roleLocation = listing_bannerGroup.find("div", class_="css-1v5elnn e11nt52q2").getText()
        except:
            company_roleLocation = "NA"

        ##############################################################################################################

        # Définition du chemin vers le pilote Chrome WebDriver
        # driver_path = 'C:\\Users\\gaspa\\Downloads\\chromedriver_win32\\chromedriver.exe'
        # driver_path = 'h:\\Downloads\\chromedriver_win32 (1)\\chromedriver.exe'

        # Instanciation du navigateur
        driver = webdriver.Chrome()
        driver.get(requested_url)

        # Localisation du span en cliquant dessus
        span_locator = (By.CSS_SELECTOR, 'span.link.py-xsm.px-std')
        text_to_find = 'Company'

        try:
            span_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(span_locator)
            )
            if text_to_find in span_element.text:
                span_element.click()
            else:
                print("Le texte spécifié n'est pas présent dans le span.")
        except:
            print("Erreur lors de la recherche du span")
            headquarters = "NA"
            size = "NA"
            type = "NA"
            revenue = "NA"

        # Obtention du contenu HTML de la page
        html_content = driver.page_source

        # Création de l'objet BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Extraction des informations sur l'entreprise
        entreprise_div = soup.find('div', id='InfoFields')

        try:
            # Récupération des différentes informations à l'intérieur du div
            headquarters_element = entreprise_div.find('span', id='headquarters')
            headquarters = headquarters_element.text.strip() if headquarters_element else "NA"

            size_element = entreprise_div.find('span', id='size')
            size = size_element.text.strip() if size_element else "NA"

            type_element = entreprise_div.find('span', id='type')
            type = type_element.text.strip() if type_element else "NA"

            revenue_element = entreprise_div.find('span', id='revenue')
            revenue = revenue_element.text.strip() if revenue_element else "NA"
        except:
            print("Erreur lors de l'extraction des informations sur l'entreprise")
            headquarters = "NA"
            size = "NA"
            type = "NA"
            revenue = "NA"

        # Fermeture du navigateur
        driver.quit()

    return companyName, company_starRating, company_offeredRole, company_roleLocation, headquarters, size, type, revenue


# extracts desired data from listing description
def extract_listingDesc(listing_soup):
    extract_listingDesc_tmpList = []
    listing_jobDesc_raw = None

    try:
        listing_jobDesc_raw = listing_soup.find("div", id="JobDescriptionContainer")
        if type(listing_jobDesc_raw) != type(None):
            JobDescriptionContainer_found = True
        else:
            JobDescriptionContainer_found = False
            listing_jobDesc = "NA"
    except Exception as e:
        print("[ERROR] {} in extract_listingDesc".format(e))
        JobDescriptionContainer_found = False
        listing_jobDesc = "NA"

    if JobDescriptionContainer_found:
        jobDesc_items = listing_jobDesc_raw.findAll('li')
        for jobDesc_item in jobDesc_items:
            extract_listingDesc_tmpList.append(jobDesc_item.text)

        listing_jobDesc = " ".join(extract_listingDesc_tmpList)

        if len(listing_jobDesc) <= 10:
            listing_jobDesc = listing_jobDesc_raw.getText()

    return listing_jobDesc


# extract data from listing
def extract_listing(url):
    request_success = False
    try:
        listing_soup, requested_url = requestAndParse(url)
        request_success = True
    except Exception as e:
        print("[ERROR] Error occurred in extract_listing, requested url: {} is unavailable.".format(url))
        return ("NA", "NA", "NA", "NA", "NA", "NA")

    if request_success:
        companyName, company_starRating, company_offeredRole, company_roleLocation, headquarters, size, type, revenue = extract_listingBanner(listing_soup, requested_url)
        listing_jobDesc = extract_listingDesc(listing_soup)

        return (companyName, company_starRating, company_offeredRole, company_roleLocation, headquarters, size, type, revenue, listing_jobDesc, requested_url)


if __name__ == "__main__":
    
    url = "https://www.glassdoor.sg/job-listing/senior-software-engineer-java-scala-nosql-rakuten-asia-pte-JV_KO0,41_KE42,58.htm?jl=1006818844403&pos=104&ao=1110586&s=58&guid=00000179d5112735aff111df641c01be&src=GD_JOB_AD&t=SR&vt=w&ea=1&cs=1_c8e7e727&cb=1622777342179&jobListingId=1006818844403&cpc=AF8BC9077DDDE68D&jrtk=1-1f7ah29sehimi801-1f7ah29t23ogm000-80a84208d187d367&jvt=aHR0cHM6Ly9zZy5pbmRlZWQuY29tL3JjL2dkL3BuZz9hPUh5MlI4ekNxUWl3d19sM3FuaUJHaFh3RlZEYUJyUWlpeldIM2VBR1ZHTUVSeUk5VEo1ZTEzWWl5dU1sLWJWX0NIeGU4NjBDc3o0dE5sV3ZLT2pRTHFIZU5KTHpPLUhLeEFRSERmeE5CdHNUTUc1RV9FSFR2VW5FNldmWWxJQVp5dXIzNFRZZjIzLWNWNXE0NnRhSTF3V1pKeW54dHhNUkxVRlhEekI2djYwMVZGWl9vbGU5andSYjVhX3BvT0cza0JJb0NYQXo0TVZhNWdvUFY4dXY3WVJTYlMySUpZTVpyR252dEc3ZFM1aXlFQ09icHI0YVRKU2ZLUzkzMUxmLXpyQjFlZHZxbHBxbElZMXhpRksxZmdIMEhFLTJBN2pySHRZa1g0aDJCWGRxTzBCdDM0bDNzWlJDLWIxaUlCT0xnZFh6bjg4cnNjZ1N0V1BHdVhNVm5xT3A3Q0s1UEEtb0QxWDl0WFhkY19WM3Fic0dSS0tfZi1oVUZyUUlrc0o2ZV9yVHNjaFpRVkIyV2V1bmRBejNYQWVPcFZNb3lqZFlONWpLUTdVbDUxTlU5LXFVWnZIT19VWlNEWDVtdVYwR3dNbWpXVDFyaHhMM3ZkcUZqcnM4WDZuc3BYYUhYcHg1dXNUVTVJODdzQk12Q2owaXkxTmRjUmhNXzU2TF9KbXNlY0VzajNWWmFOMDQ3QmNSWU5HSGNFNmctcXUzRUV4bHJrdjQxQ3QteW02ZFo5bE45XzBfb3prR2NBVkdqQU9kaS1UNWRwVnllYzA1OU53Q3Aya2QwdHdoRU5kUnU5UzNlTUR5WmJOSFZGb0t3MnR6V1lKbTllaGxuS3hTMEdoMDhLekVBWGg4OW9BblZGR2U2ajRtMUw3T29CSVNvZWVZaC0wRHRoSTV4eUV0ODJCRERkeTV3QlREUVNTUUZ1Mkp3WUEyRE9qZk5udk5xbzQwaVZKRmF0VWFlVDc2TFl6bnIwQTB2RWRGZlNORE41QmlUaHI3VmgyUWs3bkRGaVFibmUzcWlqZE1ZYzR5TmVYZUhnUFFmOHEwc1Q2aHJrX0hPX1RwbWI5M21hd2hxOEd6a2lEaFMtUQ&ctt=1622777391568"
    start_time = time()
    returned_tuple = extract_listing(url)
    time_taken = time() - start_time
    print(returned_tuple)
    print("[INFO] returned in {} seconds".format(time_taken))