% Molicel P28A parameters

CapAh = 2.8; % Capacity measured in Amp Hours
%CapWh = 10.3 % Capacity measured in Watt Hours

IChargeMax = 6; % Maximum Charging Current
%IChargeAvg = 2.8 % Average Charging Current
IDisMax = 35; % Max Discharge Current
%Vmax = 4.2 % Max Voltage
%Vnom = 3.6 % Nominal Voltage
%Vmin = 2.5 % Minimum Voltage
R0 = .02; % Maximum Internal Resistance
an1 = 0;
flag = 0;
while ((an1 ~e= 'c')&&(an1 ~= 'd'))
    if flag == 1
        fprintf("Invalid Input\n")
    end
    prompt  = "Are you charging or discharging your pack? (c/d) ";
    an1 = input(prompt, "s");
    flag = 1;
end


prompt = "What is your charging or discharging current? ";
Iin = input(prompt);
if (Iin > IDisMax && an1 == 'd') || ( Iin > IChargeMax && an1 == 'c')
    disp(an1)
    fprintf("Not Possible\n")

else
    timeh = CapAh/Iin;
    power = (Iin^2)*R0;
    timeMin = timeh * 60;
    if an1 == 'd'
        cord = "Discharged";
    else
        cord = "Charged";
    end
    fprintf("Your cell %s in %s hours or %s mins \n", cord, num2str(timeh), num2str(timeMin))
    fprintf("Power Disipated: %sW", num2str(power))
end


