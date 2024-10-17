'''
 2019 Bjoern Annighoefer
'''

from .domain import Domain
from ..util.logger import NoLogging,LogLevels
from ..serialization import TextSerializer
from ..command.command import Get
from ..event import ALL_EVENT_TYPES

class CmdRunnerBasedDomain(Domain):
    def __init__(self,cmdRunner,logger=NoLogging(),serializer=TextSerializer(),enableBenchmark=False):
        super().__init__(logger)
        self.serializer = serializer
        self.enableBenchmark = enableBenchmark
        self.doCounter = 0
        self.cmdRunner = cmdRunner
        self.callManager = cmdRunner.callManager #create a reference on domain level in order to ensure compatibility to multiprocess wrappers.
        self.defaultSessionId = None #this can be set to prevent transporting the session to every Do call
        
    def RawDo(self,cmd,sessionId=None):
        self.doCounter += 1
        usedSessionId = sessionId if None!=sessionId else self.defaultSessionId
        self.logger.PassivatableLog(LogLevels.INFO,lambda : "cmd: %s"%(self.serializer.serialize(cmd)))
        res = self.cmdRunner.Exec(cmd,usedSessionId)
        return res
        
    def Get(self,target):
        cmd = Get(target)
        res = self.Do(cmd)
        return res
    
    #Override the event provid methods since the sole event provider shall be the cmd runner
    #@Override
    def Observe(self,callback,eventTypes=ALL_EVENT_TYPES,context=None,sessionId=None): #by default register for all events
        self.cmdRunner.Observe(callback,eventTypes,context,sessionId)
    
    #@Override    
    def Unobserve(self,callback,context=None):
        self.cmdRunner.Unobserve(callback,context)
        
    #@Override
    def NotifyObservers(self,evts,excludedCallback=None,excludedContext=None):
        self.cmdRunner.NotifyObservers(evts,excludedCallback,excludedContext)
        
    def Close(self):
        #benchmark:
        if self.enableBenchmark:
            self.cmdRunner.benchmark.SaveToFile('CmdBenchmark.csv')
            self.logger.Info("Command benchmark saved to CmdBenchmark.csv")
            self.cmdRunner.qryEvaluator.benchmark.SaveToFile('QryBenchmark.csv')
            self.logger.Info("Query segment benchmark saved to QryBenchmark.csv")
            
    def SetDefaultSessionId(self,sessionId):
        ''' Sets the session Id used if no session id is provided
        '''
        self.defaultSessionId = sessionId
            
    