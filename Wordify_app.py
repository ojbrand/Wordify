
import plotly.graph_objects as go
from Wordify import Wordify
import Wordify_parsers as tp
import pprint as pp

def main():

    wordify = Wordify()
    wordify.load_stop_words('stop_words.txt')
    wordify.load_text('songs/HWMTF.txt', 'HWMTF')
    wordify.load_text('songs/lithonia.txt', 'Lithonia')
    wordify.load_text('songs/steps_beach.txt', 'Steps Beach')
    wordify.load_text('songs/TMS.txt', 'TMS')
    wordify.load_text('songs/survive.txt', 'Survive')
    # wordify.create_sankey_diagram(k=25)
    wordify.create_sankey_diagram()
    #wordify.create_heatmap()
    wordify.create_word_length_hist()
    #wordify.load_text('myfile.json', 'J', parser=tp.json_parser)

    # pp.pprint(wordify.data)








if __name__ == '__main__':
    main()

