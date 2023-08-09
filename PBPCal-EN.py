import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


def calculate_tab1():
    # 获取用户输入的参数值
    flow_rate = float(entry_flow_rate.get())
    head = float(entry_head.get())
    power_factor = float(entry_power_factor.get())

    # 执行计算逻辑
    absorbed_power = flow_rate * head / 3.6*9.81 / 1000 / power_factor*100
    motor_power_options = [0.25, 0.37, 0.55, 0.75, 1.1, 1.5, 2.2, 3.0, 4.0, 6, 8, 11, 15, 19, 22, 30, 37, 45, 55, 75, 90, 110, 132, 160, 200, 250, 315]
    if absorbed_power/0.95 >= 315:
        result_label_absorbed_power_tab1.config(text="Too large, please check!",justify='center')
        result_label_absorbed_power_tab1.grid(row=4, column=1)
        return

    motor_power = min(filter(lambda x: x >= absorbed_power/0.95, motor_power_options))
    
    # 显示计算结果
    result_label_absorbed_power_tab1.config(text="Absorbed Power: {:.2f} kW".format(absorbed_power),justify='center')
    result_label_absorbed_power_tab1.grid(row=4, column=1)  # 将结果放置在第1列
    result_label_motor_power_tab1.config(text="Motor Power: {:.2f} kW".format(motor_power),justify='center')
    result_label_motor_power_tab1.grid(row=5, column=1)  # 将结果放置在第1列

def calculate_tab2():
    # 获取用户输入的参数值
    airflow = float(entry_airflow.get())
    pressure = float(entry_pressure.get())
    power_factor = float(entry_power_factor_tab2.get())    

    # 执行计算逻辑
    absorbed_power = airflow*pressure*1000/102/3600/power_factor*100 # 根据需求编写计算代码
    motor_power_options = [0.25, 0.37, 0.55, 0.75, 1.1, 1.5, 2.2, 3.0, 4.0, 6, 8, 11, 15, 19, 22, 30, 37, 45, 55, 75, 90, 110, 132, 160, 200, 250, 315]
    if absorbed_power >= 315:
        result_label_absorbed_power_tab2.config(text="Too large, please check!",justify='center')
        result_label_absorbed_power_tab2.grid(row=4, column=1)
        return
    motor_power = min(filter(lambda x: x >= absorbed_power/0.95, motor_power_options))
    
    # 显示计算结果
    result_label_absorbed_power_tab2.config(text="Absorbed Power: {:.2f} kW".format(absorbed_power),justify='center')
    result_label_absorbed_power_tab2.grid(row=4, column=1)  # 将结果放置在第1列
    result_label_motor_power_tab2.config(text="Motor Power: {:.2f} kW".format(motor_power),justify='center')
    result_label_motor_power_tab2.grid(row=5, column=1)  # 将结果放置在第1列

def calculate_tab3():
    # 获取用户输入的参数值
    flow_rate = float(entry_flow_rate_tab3.get())
    dimeter= entry_dimeter_tab3.get()
    
    inner_diameter = {
        "15": 15,
        "20": 19,
        "25": 26,
        "32": 31,
        "40": 38,
        "50": 50,
        "65": 68,
        "80": 81,
        "100": 100,
        "125": 124,
        "150": 150,
        "200": 207,
        "250": 257,
        "300": 309,
        "350": 357,
        "400": 406,
        "450": 456,
        "500": 506,
        "600": 618,
        "700": 708,
        "800": 804,
        "900": 904,
        "1000": 1004,
        "1200": 1200
    }

    
    # 执行计算逻辑
    if str(dimeter) not in inner_diameter:
        result_label_pipevelocity_tab3.config(text="Wrong diameter, please check!",justify='center')
        result_label_pipevelocity_tab3.grid(row=4, column=1)
        return
    
    inner_dia = inner_diameter[str(dimeter)]
    pipevelocity = flow_rate*4/3.1415926/inner_dia**2/3600*1000*1000

    pressure_pipe_dimeter=pow((flow_rate*4/3600/3.1415926/2),0.5)*1000
    gravity_pipe_dimeter=pow((flow_rate*4/3600/3.1415926/0.6),0.5)*1000


    # 显示计算结果
    result_label_pipevelocity_tab3.config(text="Velocity is: {:.2f} m/s".format(pipevelocity),justify='center')
    result_label_pipevelocity_tab3.grid(row=4, column=1)  # 将结果放置在第1列

    result_label_pressure_pipe_dimeter_tab3.config(text="2.0m/s Diameter: {:.0f} mm".format(pressure_pipe_dimeter),justify='center')
    result_label_pressure_pipe_dimeter_tab3.grid(row=5, column=1)  # 将结果放置在第1列

    result_label_gravity_pipe_dimeter_tab3.config(text="0.6m/s Diameter: {:.0f} mm".format(gravity_pipe_dimeter),justify='center')
    result_label_gravity_pipe_dimeter_tab3.grid(row=6, column=1)  # 将结果放置在第1列
        

# 创建窗口和标签页
window = tk.Tk()
window.title("Calculator")

# 设置等线字体
font = tkFont.Font(family="等线", size=12)

# 创建标签页控件
tab_control = ttk.Notebook(window)

# 创建第一页的标签页
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Pump Power')

label_flow_rate = tk.Label(tab1, text="Flow (m³/h):", font=font)
label_flow_rate.grid(row=0, column=0)
entry_flow_rate = tk.Entry(tab1, font=font)
entry_flow_rate.grid(row=0, column=1)

label_head = tk.Label(tab1, text="Head (m):", font=font)
label_head.grid(row=1, column=0)
entry_head = tk.Entry(tab1, font=font)
entry_head.grid(row=1, column=1)

label_power_factor = tk.Label(tab1, text="Efficiency (%):", font=font)
label_power_factor.grid(row=2, column=0)
entry_power_factor = tk.Entry(tab1, font=font)
entry_power_factor.grid(row=2, column=1)

calculate_button_tab1 = tk.Button(tab1, text="Calculate", command=calculate_tab1, font=(font["family"], font["size"], "bold"))
calculate_button_tab1.grid(row=3, column=1, sticky="nsew")

result_label_absorbed_power_tab1 = tk.Label(tab1, text="", font=font,justify='left')
result_label_absorbed_power_tab1.grid(row=4, column=1)

result_label_motor_power_tab1 = tk.Label(tab1, text="", font=font,justify='left')
result_label_motor_power_tab1.grid(row=5, column=1)



# 创建第二个标签页的内容
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Blower Power')

label_airflow = tk.Label(tab2, text="Airflow (Nm³/h):", font=font)
label_airflow.grid(row=0, column=0)
entry_airflow = tk.Entry(tab2, font=font)
entry_airflow.grid(row=0, column=1)

label_pressure = tk.Label(tab2, text="Head (m):", font=font)
label_pressure.grid(row=1, column=0)
entry_pressure = tk.Entry(tab2, font=font)
entry_pressure.grid(row=1, column=1)

label_power_factor_tab2 = tk.Label(tab2, text="Efficiency (%):", font=font)
label_power_factor_tab2.grid(row=2, column=0)
entry_power_factor_tab2 = tk.Entry(tab2, font=font)
entry_power_factor_tab2.grid(row=2, column=1)

calculate_button_tab2 = tk.Button(tab2, text="Calculate", command=calculate_tab2, font=(font["family"], font["size"], "bold"))
calculate_button_tab2.grid(row=3, column=1, sticky="nsew")

result_label_absorbed_power_tab2 = tk.Label(tab2, text="", font=font,justify='left')
result_label_absorbed_power_tab2.grid(row=4, column=1)

result_label_motor_power_tab2 = tk.Label(tab2, text="", font=font,justify='left')
result_label_motor_power_tab2.grid(row=5, column=1)



# 创建第三页的标签页
tab3= ttk.Frame(tab_control)
tab_control.add(tab3, text='Pipe Diameter')

label_flow_rate_tab3 = tk.Label(tab3, text="Flow (m³/h):", font=font)
label_flow_rate_tab3.grid(row=0, column=0)
entry_flow_rate_tab3 = tk.Entry(tab3, font=font)
entry_flow_rate_tab3.grid(row=0, column=1)

label_dimeter_tab3 = tk.Label(tab3, text="Diameter (mm):", font=font)
label_dimeter_tab3.grid(row=1, column=0)
entry_dimeter_tab3 = tk.Entry(tab3, font=font)
entry_dimeter_tab3.grid(row=1, column=1)

calculate_button_tab3 = tk.Button(tab3, text="Calculate", command=calculate_tab3, font=(font["family"], font["size"], "bold"))
calculate_button_tab3.grid(row=3, column=1, sticky="nsew")

result_label_pipevelocity_tab3 = tk.Label(tab3, text="Velocity: ", font=font,justify='left')
result_label_pipevelocity_tab3.grid(row=4, column=1)

result_label_pressure_pipe_dimeter_tab3 = tk.Label(tab3, text="", font=font,justify='left')
result_label_pressure_pipe_dimeter_tab3.grid(row=5, column=1) # 将结果放置在第1列

result_label_gravity_pipe_dimeter_tab3 = tk.Label(tab3, text="", font=font,justify='left')
result_label_gravity_pipe_dimeter_tab3.grid(row=6, column=1)  # 将结果放置在第1列


# 设置窗体大小
window.geometry("320x200")


# 将标签页控件添加到窗口中
tab_control.pack(expand=1, fill='both')

window.mainloop()


