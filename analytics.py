import matplotlib.pyplot as plt


class Analytics:

    def battery_chart(self, values):

        plt.plot(values)

        plt.xlabel('Time')

        plt.ylabel('Battery')

        plt.title('Robot Battery Usage')

        plt.savefig(

            'outputs/battery_chart.png'

        )

        print("Chart Saved")
