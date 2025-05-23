setup: ## Activates virtual environment and installs dependencies
	poetry shell
	poetry install

scrape: ## Runs the srapy command to scrape the website
	@{\
		pushd src/retriever ;\
		scrapy crawl TvPrice --overwrite-output ProductPage.json ;\
		popd ;\
	}

run: setup scrape # sets everything up