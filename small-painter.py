# -*- coding: utf-8 -*-
from core import CardPainter

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame, KeepInFrame


class SmallCardPainter(CardPainter):

    def __init__(self, input_path, output_path, fontname, fontpath):
        CardPainter.__init__(self, input_path, output_path, fontname, fontpath,
                             is_landscape=True, padding=10)

    def paint(self):
        for story in self.backlog:
            self.__paint_story_card(story)
        self.canvas.save()

    def get_origin(self, card_index):
        i = (card_index - 1) % 4
        if i == 0:
            x, y = 0, self.page_height / 2
        elif i == 1:
            x, y = self.page_width / 2, self.page_height / 2
        elif i == 2:
            x, y = 0, 0
        else:
            x, y = self.page_width / 2, 0
        return x + self.padding, y + self.padding

    def get_size(self):
        return self.page_width / 2 - self.padding * 2,\
               self.page_height / 2 - self.padding * 2

    def __paint_story_card(self, story):
        self.story_count += 1

        if self.story_count % 4 == 1 and self.story_count > 1:
            self.canvas.showPage()

        x0, y0 = self.get_origin(self.story_count)
        sx, sy = self.get_size()

        # background
        self.canvas.setFillGray(self.lite_gray)
        self.canvas.setLineWidth(2)
        self.canvas.setStrokeGray(self.black)
        self.canvas.rect(x0, y0, sx, sy, stroke=1, fill=1)
        self.canvas.setLineWidth(1)

        style = ParagraphStyle('normal', fontName=self.fontname, fontSize=18, leading=24, textColor=[self.white]*3)

        # How to demo
        self.canvas.setFillGray(self.gray)
        self.canvas.rect(x0+1, y0+1, sx-2, 80, stroke=0, fill=1)
        self.canvas.setFillGray(self.white)
        text = [Paragraph(story.demo, style)]
        text_inframe = KeepInFrame(sx-2, 80, text)
        frame = Frame(x0+1, y0+1, sx-2, 80)
        frame.addFromList([text_inframe], self.canvas)

        # Notes
        self.canvas.setFillGray(self.gray)
        self.canvas.rect(x0+1, y0+101, sx-2, 80, stroke=0, fill=1)
        self.canvas.setFillGray(self.white)
        text = [Paragraph(story.notes, style)]
        text_inframe = KeepInFrame(sx-2, 80, text)
        frame = Frame(x0+1, y0+101, sx-2, 80)
        frame.addFromList([text_inframe], self.canvas)

        # ID
        self.canvas.setFillGray(self.black)
        self.canvas.rect(x0, y0+248, 50, 30, stroke=0, fill=1)
        self.setFontSize(20)
        self.canvas.setFillGray(self.lite_gray)
        self.canvas.drawString(x0+6, y0+256, '#%s' % story.sid)

        self.setFontSize(13)
        self.canvas.setFillGray(self.gray)
        self.canvas.drawString(x0+6, y0+185, 'How to demo')
        self.canvas.drawString(x0+6, y0+85, 'Notes')

        # Name
        style = ParagraphStyle('normal', fontName=self.fontname, fontSize=28,
                               leading=29, textColor=[self.black]*3)
        text = [Paragraph(story.name, style)]
        text_inframe = KeepInFrame(sx, 47, text)
        frame = Frame(x0, y0+201, sx, 47)
        frame.addFromList([text_inframe], self.canvas)

        # Estimate
        self.canvas.setFillGray(self.gray)
        self.setFontSize(16)
        self.canvas.drawString(x0+346, y0+256, 'Est: %s' % story.est)


def main():
    input_path = 'input.csv'
    output_path = 'small-cards.pdf'
    fontname = 'msyh'
    fontpath = 'assets/msyh.ttf'

    painter = SmallCardPainter(input_path, output_path, fontname, fontpath)
    painter.paint()


if __name__ == '__main__':
    main()
