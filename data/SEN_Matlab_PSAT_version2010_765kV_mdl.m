Bus.con = [ ... 
  1  765  1  0  1  1;
  2  765  1  0  1  1;
  3  765  1  0  1  1;
  4  765  1  0  1  1;
  5  765  1  0  1  1;
  6  765  1  0  1  1;
  7  765  1  0  1  1;
 ];

% csvwrite('Bus.csv',Bus.con)

Line.con = [ ... 
  4  1  100  765  60  161  0  0.012  0.0008727  1.320457e-008  0  0  121.5  110.5  121.5  1;
  4  1  100  765  60  161  0  0.012  0.0008727  1.320457e-008  0  0  121.5  110.5  121.5  1;
  3  2  100  765  60  65  0  0.012  0.0008727  1.320457e-008  0  0  301  273.7  301  1;
  4  1  100  765  60  161  0  0.012  0.0008727  1.320457e-008  0  0  121.5  110.5  121.5  1;
  5  4  100  765  60  225  0  0.012  0.0008727  1.320457e-008  0  0  87  79.1  87  1;
  6  5  100  765  60  182  0  0.012  0.0008727  1.320457e-008  0  0  107.5  97.7  107.5  1;
  5  4  100  765  60  225  0  0.012  0.0008727  1.320457e-008  0  0  87  79.1  87  1;
  6  3  100  765  60  90  0  0.012  0.0008727  1.320457e-008  0  0  217  198  217  1;
  2  7  100  765  60  123  0  0.012  0.0008727  1.320457e-008  0  0  159.1  144.6  159.1  1;
  2  5  100  765  60  270  0  0.012  0.0008727  1.320457e-008  0  0  72.5  65.9  72.5  1;
  3  5  100  765  60  211  0  0.012  0.0008727  1.320457e-008  0  0  92.7  84.3  92.7  1;
  5  4  100  765  60  225  0  0.012  0.0008727  1.320457e-008  0  0  87  79.1  87  1;
  2  7  100  765  60  123  0  0.012  0.0008727  1.320457e-008  0  0  159.1  144.6  159.1  1;
 ];

Shunt.con = [ ... 
  7  100  765  60  0  -19.5075  1;
 ];

SW.con = [ ... 
  1  100  765  1.05  0  1.5  -1.5  1.1  0.9  30  1  1  1;
 ];

PV.con = [ ... 
  5  100  765  0  1.07  2.8  -3  1.1  0.9  1  1;
  3  100  765  0  1.07  2.8  -3  1.1  0.9  1  1;
 ];

PQ.con = [ ... 
  3  100  765  6.48  3.45  1.2  0.8  1  1;
  5  100  765  11.99  7.5  1.2  0.8  1  1;
  7  100  765  11.73  12.11  1.2  0.8  1  1;
  5  100  765  0.0122  4.8769  1.2  0.8  1  1;
  4  100  765  0.0163  6.5025  1.2  0.8  1  1;
 ];

PQgen.con = [ ... 
  2  100  765  12.7512  -17.2074  1.1  0.9  0  1;
  6  100  765  6.12  0.22  1.1  0.9  0  1;
 ];

Bus.names = {... 
  'Guri 765kV'; 'La Arenosa 765kV'; 'La Horqueta 765kV'; 'Malena 765kV'; 'San Geronimo 765kV'; 
  'Sur OMZ 765kV'; 'Yaracuy 765kV'};

% fid = fopen('Bus_names.csv','w')
% fprintf(fid,'%s,\n',Bus_names{:,1})
