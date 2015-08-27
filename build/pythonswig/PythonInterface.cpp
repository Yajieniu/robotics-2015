#include <Python.h>
#include <PythonInterface.h>

#include <stdio.h>

using namespace std;

VisionCore* PythonInterface::CORE_INSTANCE = NULL;
bool PythonInterface::GLOBAL_INITIALIZED = false;
std::mutex PythonInterface::PY_MUTEX;
std::mutex PythonInterface::CORE_MUTEX;

static_assert(PY_MAJOR_VERSION == 2 && PY_MINOR_VERSION == 7 && PY_MICRO_VERSION == 5, "Must compile with Python Version 2.7.5");

void PythonInterface::GlobalInit() {
  if(GLOBAL_INITIALIZED) return;
  PY_MUTEX.lock();
  const char *chome = getenv("NAO_HOME");
  const char *cuser = getenv("USER");
  string home, user, scriptPath, swigPath, corePath, modulePath, homePath;
  if(cuser) user = cuser;
  if(chome) home = chome;
  if(user == "nao") {
    scriptPath = "/home/nao/python";
    swigPath = "/home/nao/bin";
    corePath = "/usr/lib/python2.7";
    modulePath = "/lib/python2.7";
    homePath = "/usr";
  } else {
    scriptPath = home + "/core/python";
    swigPath = home + "/build/pythonswig";
    corePath = home + "/naoqi/lib/python2.7";
    modulePath = home + "/naoqi/crosstoolchain/atom/sysroot/lib/python2.7";
    homePath = home + "/naoqi";
  }

  setenv("PYTHONHOME", homePath.c_str(), 1);
  
  string pythonPath = "";
  pythonPath += scriptPath + ":";
  pythonPath += swigPath + ":";
  pythonPath += modulePath + ":";
  pythonPath += corePath;
  setenv("PYTHONPATH", pythonPath.c_str(), 1);

  printf("Starting initialization of Python version %s\n", Py_GetVersion());
  Py_InitializeEx(0); // InitializeEx(0) turns off signal hooks so ctrl c still works
  GLOBAL_INITIALIZED = true;
  PY_MUTEX.unlock();
}

void PythonInterface::Init(VisionCore* core) {
  GlobalInit();
  PY_MUTEX.lock();
  CORE_MUTEX.lock();
  CORE_INSTANCE = core;
  thread_ = Py_NewInterpreter();
  PyRun_SimpleString(
    "import pythonswig_module\n"
    "pythonC = pythonswig_module.PythonInterface().CORE_INSTANCE.interpreter_\n"
    "pythonC.is_ok_ = False\n"
    "from init import *\n"
    "init()\n"
    "pythonC.is_ok_ = True\n"
  );
  CORE_MUTEX.unlock();
  PY_MUTEX.unlock();
}

void PythonInterface::Finalize() {
  PY_MUTEX.lock();
  if(thread_ != PyThreadState_Get())
    PyThreadState_Swap((PyThreadState*)thread_);
  Py_EndInterpreter((PyThreadState*)thread_);
  PY_MUTEX.unlock();
}

void PythonInterface::Execute(string command) {
  PY_MUTEX.lock();
  if(thread_ != PyThreadState_Get())
    PyThreadState_Swap((PyThreadState*)thread_);
  PyRun_SimpleString((char*)command.c_str());
  PY_MUTEX.unlock();
}

void PythonInterface::GlobalFinalize() {
  PY_MUTEX.lock();
  Py_Finalize();
  GLOBAL_INITIALIZED = false;
  PY_MUTEX.unlock();
}
