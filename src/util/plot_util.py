import matplotlib.pyplot as plt


def plot_orig(path, x_dates, y_prices, label):
    xdates = x_dates
    plt.clf()
    plt.plot(xdates, y_prices, label=label)
    plt.legend()
    plt.savefig(f'{path}')
    plt.close()


def plot_prediction(path, x_test_date, y_test, y_pred):
    xdates = x_test_date
    plt.clf()
    plt.plot(xdates, y_test, label='True Values')
    plt.plot(xdates, y_pred, label='Predicted Values')
    plt.title('True vs Predicted Values')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.savefig(f'{path}')
    plt.close()
