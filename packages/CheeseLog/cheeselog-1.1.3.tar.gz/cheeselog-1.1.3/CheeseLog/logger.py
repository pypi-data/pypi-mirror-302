import inspect, datetime, sys, re, os, time
from typing import Dict, Set

from CheeseLog import style
from CheeseLog.level import Level

class Logger:
    def __init__(self):
        self._messageTemplate: str = '(%l) %t > %c'
        self._styledMessageTemplate: str = '(<black>%l</black>) <black>%t</black> > %c'
        self._timerTemplate: str = '%Y-%m-%d %H:%M:%S.%f'
        self._levels: Dict[str, Level] = {
            'DEBUG': Level(10),
            'INFO': Level(20, styledMessageTemplate = '(<green>%l</green>) <black>%t</black> > %c'),
            'STARTING': Level(20, styledMessageTemplate = '(<green>%l</green>) <black>%t</black> > %c'),
            'ENDING': Level(20, styledMessageTemplate = '(<green>%l</green>) <black>%t</black> > %c'),
            'LOADING': Level(20, styledMessageTemplate = '(<blue>%l</blue>) <black>%t</black> > %c'),
            'LOADED': Level(20, styledMessageTemplate = '(<cyan>%l</cyan>) <black>%t</black> > %c'),
            'BUILDING': Level(20, styledMessageTemplate = '(<blue>%l</blue>) <black>%t</black> > %c'),
            'BUILT': Level(20, styledMessageTemplate = '(<cyan>%l</cyan>) <black>%t</black> > %c'),
            'HTTP': Level(20, styledMessageTemplate = '(<blue>%l</blue>) <black>%t</black> > %c'),
            'WEBSOCKET': Level(20, styledMessageTemplate = '(<blue>%l</blue>) <black>%t</black> > %c'),
            'WARNING': Level(30, styledMessageTemplate = '(<yellow>%l</yellow>) <black>%t</black> > %c'),
            'DANGER': Level(40, styledMessageTemplate = '(<red>%l</red>) <black>%t</black> > %c'),
            'ERROR': Level(50, styledMessageTemplate = '(<magenta>%l</magenta>) <black>%t</black> > %c')
        }

        self._weightFilter: int = 0
        self._levelFilter: Set[str] = set()
        self._moduleFilter: Dict[str, int | Set[str]] = {}
        self._contentFilter: Set[str] = set()
        self._logger_weightFilter: int = 0
        self._logger_levelFilter: Set[str] = set([ 'LOADING', 'BUILDING' ])
        self._logger_moduleFilter: Dict[str, int | Set[str]] = {}
        self._logger_contentFilter: Set[str] = set()

        self._styled: bool = True

        self.filePath: str = ''

    def default(self, levelKey: str, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = False):
        if levelKey not in self.levels:
            raise KeyError('No level with this key')

        level = self.levels[levelKey]
        if level.weight < self.weightFilter:
            return

        if levelKey in self.levelFilter:
            return

        if self.moduleFilter:
            stack = inspect.stack()
            for key, value in self.moduleFilter.items():
                flag = False
                for frame in stack:
                    callingModule = frame.frame.f_locals.get('__name__')
                    if callingModule == key:
                        flag = True
                        if isinstance(value, int):
                            if level.weight <= value:
                                return
                        elif isinstance(value, Set):
                            if levelKey in value:
                                return
                        break
                if flag:
                    break

        if self.contentFilter:
            for pattern in self.contentFilter:
                if re.search(pattern, message):
                    return

        now = datetime.datetime.now()
        if sys.stdout and sys.stdout.isatty():
            if self.styled:
                _message = re.sub(r'<.+?>', lambda s: f'\033[{getattr(style, s[0][1:-1].upper())[0]}m', re.sub(r'</.+?>', lambda s: f'\033[{getattr(style, s[0][2:-1].upper())[1]}m', (level.styledMessageTemplate or self.styledMessageTemplate).replace('%t', now.strftime(self.timerTemplate)).replace('%l', levelKey).replace('%c', f'{styledMessage or message}'))).replace('\n', '\n    ')
            else:
                _message = (level.messageTemplate or self.messageTemplate).replace('%t', now.strftime(self.timerTemplate)).replace('%l', levelKey).replace('%c', f'{message}').replace('\n', '\n    ')
            if refreshed:
                _message = f'\033[F\033[K{_message}'
            print(_message.replace('&lt;', '<').replace('&gt;', '>'), end = end)

        if not self.filePath:
            return

        if level.weight < self.logger_weightFilter:
            return

        if levelKey in self.logger_levelFilter:
            return

        if self.logger_moduleFilter:
            for key, value in self.logger_moduleFilter.items():
                flag = False
                for frame in stack:
                    callingModule = frame.frame.f_locals.get('__name__')
                    if callingModule == key:
                        flag = True
                        if isinstance(value, int):
                            if level.weight <= value:
                                return
                        elif isinstance(value, Set):
                            if levelKey in value:
                                return
                        break
                if flag:
                    break

        if self.logger_contentFilter:
            for pattern in self.logger_contentFilter:
                if re.search(pattern, message):
                    return

        try:
            filePath = time.strftime(self.filePath)
        except:
            filePath = self.filePath

        os.makedirs(os.path.dirname(filePath), exist_ok = True)
        with open(filePath, 'a', encoding = 'utf-8') as f:
            f.write((level.messageTemplate or self.messageTemplate).replace('%t', now.strftime(self.timerTemplate)).replace('%l', levelKey).replace('%c', message).replace('\n', '\n    ') + '\n')

    def debug(self, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = False):
        self.default('DEBUG', message, styledMessage, end = end, refreshed = refreshed)

    def info(self, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = False):
        self.default('INFO', message, styledMessage, end = end, refreshed = refreshed)

    def starting(self, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = False):
        self.default('STARTING', message, styledMessage, end = end, refreshed = refreshed)

    def ending(self, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = False):
        self.default('ENDING', message, styledMessage, end = end, refreshed = refreshed)

    def warning(self, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = False):
        self.default('WARNING', message, styledMessage, end = end, refreshed = refreshed)

    def danger(self, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = False):
        self.default('DANGER', message, styledMessage, end = end, refreshed = refreshed)

    def error(self, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = False):
        self.default('ERROR', message, styledMessage, end = end, refreshed = refreshed)

    def websocket(self, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = False):
        self.default('WEBSOCKET', message, styledMessage, end = end, refreshed = refreshed)

    def http(self, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = False):
        self.default('HTTP', message, styledMessage, end = end, refreshed = refreshed)

    def loaded(self, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = False):
        self.default('LOADED', message, styledMessage, end = end, refreshed = refreshed)

    def loading(self, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = True):
        '''
        注意，该命令是覆盖的。
        '''

        self.default('LOADING', message, styledMessage, end = end, refreshed = refreshed)

    def built(self, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = False):
        self.default('BUILT', message, styledMessage, end = end, refreshed = refreshed)

    def building(self, message: str, styledMessage: str | None = None, *, end: str = '\n', refreshed: bool = True):
        '''
        注意，该命令是覆盖的。
        '''

        self.default('BUILDING', message, styledMessage, end = end, refreshed = refreshed)

    def encode(self, message: str) -> str:
        '''
        当消息中有`'<'`和`'>'`字符时，容易与样式格式产生冲突。使用该函数对冲突部分进行加密，可以防止冲突。
        '''

        return message.replace('<', '&lt;').replace('>', '&gt;')

    @property
    def messageTemplate(self) -> str:
        '''
        消息模版，使用占位符替换内容：

        - %l: 消息等级的key。

        - %t: 时间模版。

        - %c: 消息内容。

        该模版是默认模版。
        '''

        return self._messageTemplate

    @messageTemplate.setter
    def messageTemplate(self, value: str):
        self._messageTemplate = value

    @property
    def styledMessageTemplate(self) -> str:
        '''
        消息样式模版，与`logger.messageTemplate`相同。仅在`logger.styled == True`时生效。

        该模版是默认模版。
        '''

        return self._styledMessageTemplate

    @styledMessageTemplate.setter
    def styledMessageTemplate(self, value: str):
        self._styledMessageTemplate = value

    @property
    def timerTemplate(self) -> str:
        '''
        使用`strftime`进行日期处理。

        该模版是默认模版。
        '''

        return self._timerTemplate

    @timerTemplate.setter
    def timerTemplate(self, value: str):
        self._timerTemplate = value

    @property
    def levels(self) -> Dict[str, Level]:
        '''
        【只读】 创建一个自定义的消息等级并打印：

        ```python
        from CheeseLog import logger, Level

        logger.levels['MY_LEVEL'] = Level(40, styledMessageTemplate = '(<green>%l</green>) <black>%t</black> > %c')
        logger.default('MY_LEVEL', 'Hello World')
        ```
        '''

        return self._levels

    @property
    def weightFilter(self) -> int:
        '''
        权重过滤，优先级最高。
        '''

        return self._weightFilter

    @weightFilter.setter
    def weightFilter(self, value: int):
        self._weightFilter = value

    @property
    def levelFilter(self) -> Set[str]:
        '''
        指定消息等级过滤，优先级其次。
        '''

        return self._levelFilter

    @levelFilter.setter
    def levelFilter(self, value: Set[str]):
        self._levelFilter = value

    @property
    def moduleFilter(self) -> Dict[str, int | Set[str]]:
        '''
        指定模块的消息等级过滤，优先级再次。

        ```python
        from CheeseLog import logger

        # 两者只能选其一
        # 指定模块的消息等级权重过滤
        logger.moduleFilter['Xxx'] = 20
        # 指定模块的指定消息等级过滤
        logger.moduleFilter['Xxx'] = set([ 'DEBUG', 'WARNING' ])
        ```
        '''

        return self._moduleFilter

    @moduleFilter.setter
    def moduleFilter(self, value: Dict[str, int | Set[str]]):
        self._moduleFilter = value

    @property
    def contentFilter(self) -> Set[str]:
        '''
        对匹配的内容进行过滤，优先级最低。
        '''

        return self._contentFilter

    @contentFilter.setter
    def contentFilter(self, value: Set[str]):
        self._contentFilter = value

    @property
    def logger_weightFilter(self) -> int:
        '''
        同`logger.weightFilter`，在其之后进行日志过滤。
        '''

        return self._logger_weightFilter

    @logger_weightFilter.setter
    def logger_weightFilter(self, value: int):
        self._logger_weightFilter = value

    @property
    def logger_levelFilter(self) -> Set[str]:
        '''
        同`logger.levelFilter`，在其之后进行日志过滤。
        '''

        return self._logger_levelFilter

    @logger_levelFilter.setter
    def logger_levelFilter(self, value: Set[str]):
        self._logger_levelFilter = value

    @property
    def logger_moduleFilter(self) -> Dict[str, int | Set[str]]:
        '''
        同`logger.moduleFilter`，在其之后进行日志过滤。
        '''

        return self._logger_moduleFilter

    @logger_moduleFilter.setter
    def logger_moduleFilter(self, value: Dict[str, int | Set[str]]):
        self._logger_moduleFilter = value

    @property
    def logger_contentFilter(self) -> Set[str]:
        '''
        同`logger.contentFilter`，在其之后进行日志过滤。
        '''

        return self._logger_contentFilter

    @logger_contentFilter.setter
    def logger_contentFilter(self, value: Set[str]):
        self._logger_contentFilter = value

    @property
    def styled(self) -> bool:
        '''
        控制台是否打印样式。
        '''

        return self._styled

    @styled.setter
    def styled(self, value: bool):
        self._styled = value

logger = Logger()
