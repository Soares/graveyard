# calibre wide preferences

### Begin group: DEFAULT
 
# database path
# Path to the database in which books are stored
database_path = '/home/nate/library1.db'
 
# filename pattern
# Pattern to guess metadata from filenames
filename_pattern = u'(?P<title>.+) - (?P<author>[^_]+)'
 
# isbndb com key
# Access key for isbndb.com
isbndb_com_key = ''
 
# network timeout
# Default timeout for network operations (seconds)
network_timeout = 5
 
# library path
# Path to directory in which your library of books is stored
library_path = u'/home/nate/Media/Calibre'
 
# language
# The language in which to display the user interface
language = 'en'
 
# output format
# The default output format for ebook conversions.
output_format = 'epub'
 
# input format order
# Ordered list of formats to prefer for input.
input_format_order = cPickle.loads('\x80\x02]q\x01(U\x04EPUBq\x02U\x04MOBIq\x03U\x03LITq\x04U\x03PRCq\x05U\x03FB2q\x06U\x04HTMLq\x07U\x03HTMq\x08U\x04XHTMq\tU\x05SHTMLq\nU\x05XHTMLq\x0bU\x03ZIPq\x0cU\x03ODTq\rU\x03RTFq\x0eU\x03PDFq\x0fU\x03TXTq\x10e.')
 
# read file metadata
# Read metadata from files
read_file_metadata = True
 
# worker process priority
# The priority of worker processes. A higher priority means they run faster and consume more resources. Most tasks like conversion/news download/adding books/etc. are affected by this setting.
worker_process_priority = 'normal'
 
# swap author names
# Swap author first and last names when reading metadata
swap_author_names = False
 
# add formats to existing
# Add new formats to existing book records
add_formats_to_existing = False
 
# installation uuid
# Installation UUID
installation_uuid = '610e1607-5db3-4596-8fe4-a69d6d3c3ff6'
 
# new book tags
# Tags to apply to books added to the library
new_book_tags = cPickle.loads('\x80\x02]q\x01.')
 
# saved searches
# List of named saved searches
saved_searches = cPickle.loads('\x80\x02}q\x01.')
 
# user categories
# User-created tag browser categories
user_categories = cPickle.loads('\x80\x02}q\x01.')
 
# manage device metadata
# How and when calibre updates metadata on the device.
manage_device_metadata = 'manual'
 
# limit search columns
# When searching for text without using lookup prefixes, as for example, Red instead of title:Red, limit the columns searched to those named below.
limit_search_columns = False
 
# limit search columns to
# Choose columns to be searched when not using prefixes, as for example, when searching for Redd instead of title:Red. Enter a list of search/lookup names separated by commas. Only takes effect if you set the option to limit search columns above.
limit_search_columns_to = cPickle.loads('\x80\x02]q\x01(U\x05titleq\x02U\x07authorsq\x03U\x04tagsq\x04U\x06seriesq\x05U\tpublisherq\x06e.')
 
# migrated
# For Internal use. Don't modify.
migrated = False
 


