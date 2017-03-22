# -*- coding: utf-8 -*-
import csv

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, KeepInFrame


class CardPainter(object):

    class Story(object):
        def __init__(self, sid, name, imp, est, demo, notes):
            self.sid = sid
            self.name = name
            self.imp = imp
            self.est = est
            self.demo = demo
            self.notes = notes

    def __init__(self, input_path, output_path, fontname, fontpath):
        self.canvas = canvas.Canvas(output_path)
        self.padding = 20
        self.page_width, self.page_height = A4
        self.page = 0
        self.story_count = 0

        self.black = 0.3
        self.gray = 0.5
        self.lite_gray = 0.95
        self.white = 1

        if fontname and fontpath:
            pdfmetrics.registerFont(TTFont(fontname, fontpath))
            self.fontname = fontname
        else:
            self.fontname = 'Helvetica'

        self.load_backlog(input_path)

    def load_backlog(self, path):
        self.backlog = []
        with open(path, 'rb') as backlog_file:
            reader = csv.reader(backlog_file)
            first_line = True
            for row in reader:
                if first_line:
                    first_line = False
                    continue
                story = self.Story(row[0], row[1], row[2], row[3], row[4], row[5])
                self.backlog.append(story)
        print 'backlog:', len(self.backlog)

    def paint(self):
        for story in self.backlog:
            self.__paint_story_card(story)
        self.canvas.save()

    def __paint_story_card(self, story):
        self.story_count += 1

        if self.story_count % 2 == 1:
            if self.story_count > 1:
                self.canvas.showPage()
            x0, y0 = self.padding, self.page_height / 2 + self.padding
            x1, y1 = self.page_width - self.padding, self.page_height - self.padding
        else:
            x0, y0 = self.padding, self.padding
            x1, y1 = self.page_width - self.padding, self.page_height / 2 - self.padding

        # background
        self.canvas.setFillGray(self.lite_gray)
        self.canvas.setLineWidth(4)
        self.canvas.setStrokeGray(self.black)
        self.canvas.rect(x0, y0, x1-x0, y1-y0, stroke=1, fill=1)
        self.canvas.setFillGray(self.white)
        self.canvas.setStrokeGray(self.gray)
        self.canvas.setLineWidth(1)
        self.canvas.rect(x0+20, y0+160, 360, 100, stroke=1, fill=1)
        self.canvas.rect(x0+20, y0+20, 360, 100, stroke=1, fill=1)
        self.canvas.rect(x0+420, y0+210, 100, 80, stroke=1, fill=1)
        self.canvas.rect(x0+420, y0+90, 100, 80, stroke=1, fill=1)

        # keys
        self.__setFontSize(16)
        self.canvas.setFillGray(self.black)
        self.canvas.drawString(x0+20, y1-30, 'Backlog item #%s' % story.sid)
        self.canvas.setFillGray(self.gray)
        self.canvas.drawString(x0+20, y0+270, 'How to demo')
        self.canvas.drawString(x0+20, y0+130, 'Notes')
        self.canvas.drawString(x0+420, y0+300, 'Importance')
        self.canvas.drawString(x0+420, y0+180, 'Estimate')

        # values
        self.canvas.setFillGray(self.black)
        self.__setFontSize(36)
        self.canvas.drawString(x0+440, y0+240, story.imp)
        self.canvas.drawString(x0+440, y0+120, story.est)

        style = ParagraphStyle('normal', fontName=self.fontname, fontSize=36, leading=40, textColor=[self.black]*3)
        text = [Paragraph(story.name, style)]
        text_inframe = KeepInFrame(360, 60, text)
        frame = Frame(x0+14, y1-95, 360, 60)
        frame.addFromList([text_inframe], self.canvas)

        style = ParagraphStyle('normal', fontName=self.fontname, fontSize=18, leading=24, textColor=[self.black]*3)

        text = [Paragraph(story.demo, style)]
        text_inframe = KeepInFrame(360, 100, text)
        frame = Frame(x0+20, y0+160, 360, 100)
        frame.addFromList([text_inframe], self.canvas)

        text = [Paragraph(story.notes, style)]
        text_inframe = KeepInFrame(360, 100, text)
        frame = Frame(x0+20, y0+20, 360, 100)
        frame.addFromList([text_inframe], self.canvas)

    def __setFontSize(self, size):
        self.canvas.setFont(self.fontname, size)


def main():
    input_path = 'input.csv'
    output_path = 'output.pdf'
    fontname = 'msyh'
    fontpath = 'msyh.ttf'

    painter = CardPainter(input_path, output_path, fontname, fontpath)
    painter.paint()


if __name__ == '__main__':
    main()
