import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Globals
titleRole = Qt.UserRole+100
senderRole = Qt.UserRole+101
msgRole = Qt.UserRole+102
theme = {
    'standard': 'color: #2a2a2a;',
    'heading': 'color: #404040;',
    'accent': 'color: #2a2aaa;',
}

class MessageWidget(QWidget):
    def setup_ui(self):
        # Objects
        self.msg = QTextBrowser()
        self.msg.setStyleSheet('background: blue;') #TESTING
        self.msg.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.msg.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.msg.setMinimumHeight(0)

        # Layout
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        #self.layout.setColumnStretch(0, 1)
        #self.layout.setRowStretch(0, 1)
        self.layout.addWidget(self.msg, 0, 0)
        self.setLayout(self.layout)

    def fill_from_index(self, index):
        # Stylization
        name_style = theme['accent']
        msg_style = theme['standard']

        # Make username part of message
        username = '<span style="' + name_style + '">'
        username += index.data(senderRole) + ': '
        username += '</span>'

        # Make text part of message
        msg = '<span style="' + msg_style + '">'
        msg += index.data(msgRole)
        msg += '</span>'

        # Combine and set
        msg = username + msg
        self.msg.setText(msg)

    def desired_height(self):
        height = self.msg.document().size().height()
        height += self.msg.contentsMargins().top()
        height += self.msg.contentsMargins().bottom()
        return height

    def sizeHint(self):
        result = super().sizeHint()
        result.setHeight(self.desired_height())
        return result

class DialogWidget(QWidget):
    def setup_ui(self):
        # Labels
        self.title = QLabel()
        #self.title.setStyleSheet('background: yellow;') #TESTING
        self.sender = QLabel()
        #self.sender.setStyleSheet('background: red;') #TESTING
        self.msg = QLabel()
        #self.msg.setStyleSheet('background: blue;') #TESTING

        # Color
        self.title.setStyleSheet(theme['heading'])
        self.sender.setStyleSheet(theme['accent'])
        self.msg.setStyleSheet(theme['standard'])

        # Layout
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(10, 0, 0, 10)
        self.layout.setColumnStretch(0, 0)
        self.layout.setColumnStretch(1, 1)
        self.layout.addWidget(self.title, 0, 0, 1, 2)
        self.layout.addWidget(self.sender, 1, 0)
        self.layout.addWidget(self.msg, 1, 1)
        self.title.setMinimumSize(
            self.title.sizeHint().width(),
            self.title.sizeHint().height() * 2.5
        )
        self.setLayout(self.layout)

    def fill_from_index(self, index):
        self.title.setText(index.data(titleRole))
        self.sender.setText(index.data(senderRole) + ': ')
        self.msg.setText(index.data(msgRole))

class CustomDelegate(QStyledItemDelegate):
    def prepare(self, widget_factory, widget_filler):
        self.null_region = QRegion()
        self.widget = widget_factory()

        self.widget.setup_ui()
        self.widget_filler = widget_filler
        self.widget.setAttribute(Qt.WA_DontShowOnScreen)

    def fill(self, rect, index):
        self.widget.show()
        self.widget.setGeometry(rect)
        self.widget_filler(self.widget, index=index)
        self.widget.close()

    def paint(self, painter, option, index):
        self.fill(rect=option.rect, index=index)

        if option.state & QStyle.State_Selected:
            painter.fillRect(
                option.rect,
                option.palette.highlight(),
            )
        top_level = option.widget.window()
        target_offset = option.widget.mapTo(top_level, option.rect.topLeft())
        self.widget.render(
            painter,
            target_offset,
            self.null_region,
            QWidget.DrawChildren,
        )

    def sizeHint(self, option, index):
        import time
        # we don't want this to be firing a lot so leave this in while changing things
        print('CustomDelegate.sizeHint()', time.time())
        rect = QRect(option.rect)
        # TODO: yuck...  find something better...  than forgetting stuff for awhile...
        width = option.widget.width()
        width -= 2 * option.widget.frameWidth()
        scroll_bar = option.widget.verticalScrollBar()
        if scroll_bar.isVisible():
            width -= scroll_bar.width()
        rect.setWidth(width)

        self.fill(rect=rect, index=index)

        return self.widget.sizeHint()

if __name__ == '__main__':
    # Initialize window
    app = QApplication(sys.argv)

    # Initialize root_layout
    root = QWidget()
    root.show()
    root_layout = QGridLayout()
    root_layout.setContentsMargins(0, 0, 0, 0)
    root_layout.setSpacing(0)
    root_layout.setRowMinimumHeight(0, 400) # Both dialogs and chats
    root_layout.setColumnMinimumWidth(0, 350) # Dialogs
    root_layout.setColumnStretch(0, 0)
    root_layout.setColumnMinimumWidth(1, 500) # Chats
    root_layout.setColumnStretch(1, 1)
    root.setLayout(root_layout)

    # Initializing dialogs
    dialogs_view = QListView()
    dialogs_view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
    dialogs_view.setAlternatingRowColors(True)
    dialogs_model = QStandardItemModel(dialogs_view)
    dialogs_view.setModel(dialogs_model)
    dialogs_delegate = CustomDelegate(dialogs_view)
    dialogs_delegate.prepare(
        widget_factory = DialogWidget,
        widget_filler = DialogWidget.fill_from_index,
    )
    dialogs_view.setItemDelegateForColumn(0, dialogs_delegate)
    root_layout.addWidget(dialogs_view, 0, 0)

    # Initialize chat pane
    chat_root = QWidget()
    chat_layout = QGridLayout()
    chat_root.setLayout(chat_layout)
    chat_layout.setContentsMargins(0, 0, 0, 0)
    chat_layout.setSpacing(0)
    chat_layout.setRowStretch(0, 1) # Chat
    chat_layout.setRowStretch(1, 0) # User input
    root_layout.addWidget(chat_root, 0, 1)

    # Adding message window
    msg_view = QListView()
    msg_view.setWordWrap(True)
    msg_view.setResizeMode(QListView.Adjust)
    msg_view.setLineWidth(3)
    msg_view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
    msg_view.setAlternatingRowColors(True)
    msg_model = QStandardItemModel(msg_view)
    msg_view.setModel(msg_model)
    msg_delegate = CustomDelegate(msg_view)
    msg_delegate.prepare(
        widget_factory = MessageWidget,
        widget_filler = MessageWidget.fill_from_index,
    )
    msg_view.setItemDelegateForColumn(0, msg_delegate)
    chat_layout.addWidget(msg_view, 0, 0)

    # Adding user input box
    msg_input = QTextEdit()
    msg_input.setStyleSheet('background: blue;')
    chat_layout.addWidget(msg_input, 1, 0)

    # Add groups to groups
    for i in range(20):
        item = QStandardItem()
        item.setData('Telegram', titleRole)
        item.setData('john', senderRole)
        item.setData('msg number ' + str(i) + ' from Telegram', msgRole)
        item.setEditable(False)
        dialogs_model.appendRow(item)
    dialogs_model.item(0).setData('changed message', msgRole)

    # Add dialogs to the messages just for testing
    for i in range(3):
        item = QStandardItem()
        item.setData('john', senderRole)
        item.setData('msg number ' + str(i) + 'a '*(i+1)*100, msgRole)
        item.setEditable(False)
        msg_model.appendRow(item)

    # Exit
    sys.exit(app.exec_())
