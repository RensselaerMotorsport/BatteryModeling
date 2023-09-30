% Molicel P28A parameters

CapAh = 2.8; % Capacity measured in Amp Hours
%CapWh = 10.3 % Capacity measured in Watt Hours

IChargeMax = 6; % Maximum Charging Current
%IChargeAvg = 2.8 % Average Charging Current
IDisMax = 35; % Max Discharge Current
%Vmax = 4.2 % Max Voltage
%Vnom = 3.6 % Nominal Voltage
%Vmin = 2.5 % Minimum Voltage
%R0 = .02 % Maximum Internal Resistance

prompt = "What is you discharge current? ";
Iin = input(prompt);
if Iin > 40
    disp("Not Possible")
%{
 elseif IChargeMax < Iin && Iin <= 40
    prompt = "Are your sure about that? (yes/no) ";
    Response = input(prompt);
    if Response == "yes"
        prompt = "It may damage your cell! (yes/no) ";
        Response = input(prompt);
        if Response == "yes"
            DTimeH = CapAh/Iin;
            DtimeMin = DTimeH * 60;
        else 
            disp("good choice")
        end
    else
        disp("good choice")
    end
  %}
else
    DTimeH = CapAh/Iin;
    DtimeMin = DTimeH * 60;
    disp(["Time in Hours" DTimeH "Time in Minutes: " DtimeMin])
end


