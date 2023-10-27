%runtime???

% Pack Specs

prompt = "How many series connections does your battery have? ";
series = input(prompt);
prompt = "How many parallel connections does your battery have? ";
parallel = input(prompt);

tcells = series*parallel;

prompt = "What is the max discharge current of your cell? ";
Idismax = input(prompt);
Ipackmax = Idismax*parallel;

prompt = "what is the voltage of one cell? ";
vcell = input(prompt);
vpack = series*vcell;

prompt = "What is the capacity of one cell? ";
capcell = input(prompt);
cappack = capcell*parallel;
energy = cappack*vpack;

% Output

fprintf("Your pack will have %s cells, a voltage of %s, a max current of %s, a capacity of %s and an energy of %s", num2str(tcells), num2str(vpack), num2str(Ipackmax), num2str(cappack), num2str(energy))




