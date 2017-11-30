
#include <QMainWindow>
#include <QApplication>
#include <QDebug>

#include "main_window.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    /*qDebug() << "Hello World";*/
    
    QApplication::setApplicationName("tambi");
    
    MainWindow mainWin;
    mainWin.setWindowIcon(QIcon("../assets/icons/logo2.png"));
    mainWin.show();
    return app.exec();
}
