import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Courpus will be given using crawl

    N_PAGES = len(list(corpus))
    result = dict()


   
    if len(corpus[page]) != 0 :
        N_LINKS = len(corpus[page])

        rand_prob = (1 - damping_factor) / N_PAGES
        p_link = damping_factor / N_LINKS

                #for link in links:
                 #   result[link] = p_link

    else:
        rand_prob = (1 - damping_factor) / N_PAGES

        p_link = 0
                
               # for page in list(corpus):
                #    result[page] = rand_prob
    for file in corpus:
        if len(corpus[page]) == 0:
            result[file] = 1 / N_PAGES
        else:
            if file not in corpus[page]:
                result[file] = rand_prob
            else:
                result[file] = rand_prob + p_link

    
    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    if n < 1:
        raise TypeError("The number of samples must be at least one")
    
    listCorpus = list(corpus)
    pages = dict()

    pages = {key : 0 for key in corpus.keys()}    

    currentPage = listCorpus[random.randint(0, len(listCorpus) - 1)]
    pages[currentPage] = pages[currentPage] + 1

    for i in range(n-1):

        pagesProbabilities = transition_model(corpus, currentPage, damping_factor)
        currentPage = random.choices(list(pagesProbabilities), weights = list(pagesProbabilities.values()), k = 1 )[0]
        pages[currentPage] = pages[currentPage] + 1

       # if page == initialPage:
       #     pages[page] = pages[page] + 1
      #  for i in range(n - 1):
       #     models = transition_model(corpus, currentPage, damping_factor)
      #  for model in list(models):
       #     pass
    pages = {key : value/n for key, value in pages.items()}

    
    return pages




    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    listCorpus = list(corpus)
    listPagesConverged = dict()
    pr = dict()

    def checkIfAllConverged(list):
        for value in list.values():
            if value == False:
                return False
        return True
    
    

    def findPagesThatLink(centralPage):
        result = set()
        for page in listCorpus:
            if centralPage in corpus[page]:
                result.add(page)
        return result

    

    pr = {key : (1/len(listCorpus)) for key in listCorpus}
    listPagesConverged = {key : False for key in listCorpus}

    COMUN_FACTOR = (1-damping_factor)/len(listCorpus)

    while checkIfAllConverged(listPagesConverged) == False:
        for page in listCorpus:
            initialValue = pr[page]
            pagesThatLink = findPagesThatLink(page)
            if(len(pagesThatLink) == 0):
                pr[page] = COMUN_FACTOR
                listPagesConverged[page] = True
            else:
                sum = 0
                for pg in pagesThatLink:
                    sum += (pr[pg] / len(corpus[pg]))
                newValue = COMUN_FACTOR + (damping_factor * sum)
                pr[page] = newValue 
                if abs(newValue - initialValue) < 0.001:
                    listPagesConverged[page] = True
            print(f"{page} : {pr[page]}")
            print(listPagesConverged)
            print(f"DIFERENça : {abs(newValue - initialValue)}")
    return pr

if __name__ == "__main__":
    main()
    
