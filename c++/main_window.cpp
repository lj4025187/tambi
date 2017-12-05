
#include <QtWidgets>

#include <main_window.h>
#include <cli_widget.h>

MainWindow::MainWindow()
    : tab_widget(new QTabWidget)
{
    resize(825, 670);
    
    tab_widget->setTabsClosable(true);
    tab_widget->setMovable(true);
    
    connect(tab_widget, &QTabWidget::tabCloseRequested, this, &MainWindow::closeTab);
    
    setCentralWidget(tab_widget);
    
    for (int i; i < 10; i++)
    {
        addNewCliTab();
        setTabText(0, "bla");
    }
}

void MainWindow::closeTab(int tab_id)
{
    tab_widget->removeTab(tab_id);
}

void MainWindow::addNewCliTab()
{
    tab_widget->addTab(new QCliWidget(this), "cli");
    activateNewTab();
}

void MainWindow::addNewDualCliTab()
{
    
}

void MainWindow::addNewPythonTab()
{
    
}

void MainWindow::activateNewTab()
{
    tab_widget->setCurrentIndex(tab_widget->count()-1);
}

void MainWindow::setTabText(int tab_id, QString text)
{
    tab_widget->setTabText(tab_id, text);
}
