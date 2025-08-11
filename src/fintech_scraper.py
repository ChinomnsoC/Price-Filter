import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

def extract_fintech_companies():
    """
    Extract fintech companies from CNBC's 2025 list by category
    """
    
    # Main URL
    main_url = "https://www.cnbc.com/the-worlds-top-fintech-companies-2025/"
    
    # Headers to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Get the main page
    print("Fetching main page...")
    response = requests.get(main_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all iframe sources that contain CSV data
    iframes = soup.find_all('iframe')
    csv_urls = []
    categories = []
    
    for iframe in iframes:
        src = iframe.get('src', '')
        if 'fintech_table.html' in src and '.csv' in src:
            # Extract the CSV filename from the iframe src
            csv_match = re.search(r'list=([^?&]+\.csv)', src)
            if csv_match:
                csv_filename = csv_match.group(1)
                # Build the direct CSV URL
                base_csv_url = "https://fm.cnbc.com/applications/cnbc.com/resources/styles/skin/special-reports/statista/fintechs25/"
                csv_url = base_csv_url + csv_filename
                csv_urls.append(csv_url)
                
                # Try to determine category from filename or nearby elements
                category = determine_category_from_filename(csv_filename)
                categories.append(category)
    
    # If we can't find CSV URLs in iframes, try direct CSV approach
    if not csv_urls:
        print("No CSV URLs found in iframes. Trying direct CSV approach...")
        csv_urls, categories = get_direct_csv_urls()
    
    # Download and process each CSV
    all_companies = {}
    
    for csv_url, category in zip(csv_urls, categories):
        print(f"Fetching {category} companies from: {csv_url}")
        try:
            # Add a small delay to be respectful
            time.sleep(1)
            
            # Try to fetch the CSV directly
            csv_response = requests.get(csv_url, headers=headers)
            
            if csv_response.status_code == 200:
                # Save to temporary file and read with pandas
                with open(f'temp_{category}.csv', 'wb') as f:
                    f.write(csv_response.content)
                
                # Read the CSV
                df = pd.read_csv(f'temp_{category}.csv')
                print(f"Found {len(df)} companies in {category}")
                
                all_companies[category] = df
                
            else:
                print(f"Failed to fetch {category}: Status {csv_response.status_code}")
                
        except Exception as e:
            print(f"Error fetching {category}: {str(e)}")
    
    return all_companies

def determine_category_from_filename(filename):
    """
    Determine category from CSV filename
    """
    category_mapping = {
        'pay.csv': 'Payments',
        'neo.csv': 'Neobanking', 
        'alt.csv': 'Alternative Financing',
        'wealth.csv': 'Wealth Technology',
        'digital.csv': 'Digital Assets',
        'enterprise.csv': 'Enterprise Fintech',
        'insurance.csv': 'Insurtech',
        'regtech.csv': 'Regulatory Technology'
    }
    
    return category_mapping.get(filename, filename.replace('.csv', '').title())

def get_direct_csv_urls():
    """
    Try direct CSV URLs based on common naming patterns
    """
    base_url = "https://fm.cnbc.com/applications/cnbc.com/resources/styles/skin/special-reports/statista/fintechs25/"
    
    # Common CSV filenames based on categories
    csv_files = [
        ('pay.csv', 'Payments'),
        ('neo.csv', 'Neobanking'),
        ('alt.csv', 'Alternative Financing'),
        ('wealth.csv', 'Wealth Technology'),
        ('digital.csv', 'Digital Assets'),
        ('enterprise.csv', 'Enterprise Fintech'),
        ('insurance.csv', 'Insurtech'),
        ('regtech.csv', 'Regulatory Technology')
    ]
    
    csv_urls = [base_url + filename for filename, _ in csv_files]
    categories = [category for _, category in csv_files]
    
    return csv_urls, categories

def save_results(companies_dict):
    """
    Save results to Excel file with separate sheets for each category
    """
    with pd.ExcelWriter('cnbc_fintech_companies_2025.xlsx', engine='openpyxl') as writer:
        
        # Create summary sheet
        summary_data = []
        for category, df in companies_dict.items():
            summary_data.append({
                'Category': category,
                'Number of Companies': len(df),
                'Sample Companies': ', '.join(df.iloc[:3, 0].tolist()) if len(df) > 0 else 'No data'
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Create separate sheet for each category
        for category, df in companies_dict.items():
            # Clean sheet name (Excel has limitations)
            sheet_name = category.replace(' ', '_')[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"Results saved to 'cnbc_fintech_companies_2025.xlsx'")

def main():
    """
    Main execution function
    """
    print("Starting CNBC Fintech Companies extraction...")
    
    # Extract companies
    companies = extract_fintech_companies()
    
    if companies:
        print(f"\nSuccessfully extracted data for {len(companies)} categories:")
        for category, df in companies.items():
            print(f"  - {category}: {len(df)} companies")
        
        # Save results
        save_results(companies)
        
        # Display sample data
        print("\nSample data:")
        for category, df in companies.items():
            print(f"\n{category} (first 5):")
            print(df.head().to_string(index=False))
    
    else:
        print("No data extracted. You may need to:")
        print("1. Check if the CSV URLs are correct")
        print("2. Handle any authentication/rate limiting")
        print("3. Manually inspect the page structure")

if __name__ == "__main__":
    main()