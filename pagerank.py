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
    result = set()

    for file in list(corpus):
        if file == page:
            if len(corpus[file]) != 0 :
                links = list(corpus[file])
                N_LINKS = len(corpus[file])

                p_self = (1 - damping_factor) / N_PAGES
                p_link = (1 - p_self) / N_LINKS

                result[file] = p_self
                for link in links:
                    result[link] = p_link

            else:
                prob = (1 - damping_factor) / N_PAGES
                for page in list(corpus):
                    result[page] = prob
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
    
    def addToCounter(counter, item):
        pass

    pages = set()

    listCorpus = list(corpus)
    for elem in listCorpus:
        pages.add({elem : 0})
    
    firstSample = listCorpus[random.randint(0, len(listCorpus) - 1)]
    currentPage = firstSample
    for page in pages:
        if page == firstSample:
            pages[page] = pages[page] + 1
    for i in range(n - 1):
        models = transition_model(corpus, currentPage, damping_factor)
        for model in list(models):





    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
