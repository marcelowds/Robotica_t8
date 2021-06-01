import numpy as np
import pylab
import random
import matplotlib.pyplot as plt

#Parametros da aquisicao
R=3# Raio de alcance do sonar
map_size=40#tamanho do mapa
sigmaR=1#desvio padrao das medidas na direcao radial
sigmaTheta=0.3#desvio padrao das medidas na direcao angular
sigmax=2#desvio padrao na direcao x
sigmay=2#desvio padrao na direcao y
#definicao das matrizes usadas
SD=[]#auxiliar
PR=[]#auxiliar
ME=[]#mapa estimado
MR=np.zeros((map_size,map_size))#mapa real

#Definicao do mapa
MR[35,5:35]=1
MR[5,15:35]=1
MR[5:35,5]=1
MR[5:35,35]=1
MR[5:20,15]=1
MR[20,15:17]=1
MR[20,22:35]=1

#Funcoes
def normal(mu,sigma,x):
  return (1/(sigma*np.sqrt(2*np.pi))*np.exp(-(x-mu)**2/(2*sigma**2)))
  
#Recebe a posicao (x,y) do sensor e posição (i,j) estimada do obstaculo
#e preenche os vizinhos com a distribuicao de probabilidade
def calc_prob(x,y,i,j):
  ds=1
  PR=np.zeros((map_size,map_size))
  for k in range (i-ds*sigmax,i+ds*sigmax+1):
    for l in range(j-ds*sigmay,j+ds*sigmay+1):
      if 0<=k and k< map_size and 0<=l and l< map_size:
        r1=np.sqrt((x-i)*(x-i)+(y-j)*(y-j))
        r2=np.sqrt((x-k)*(x-k)+(y-l)*(y-l))
        theta1=np.arctan2((j-y),(i-x))
        theta2=np.arctan2((l-y),(k-x))
        
        if (theta1*theta2<0):
          t2=max(theta1,theta2)
          t1=min(theta1,theta2)+np.pi*2
          theta1=t1
          theta2=t2                
        #if l<y and k>x:#correcoes no theta devido a tangente
        #  print(theta1,theta2,k,l)  
          #theta1=theta1-np.pi*2
        PR[k,l]=normal(r1,sigmaR,r2)*normal(theta1,sigmaTheta,theta2)

  return PR

#Faz a medida com os sensores num raio R           
def grade(x,y,ME):
  entrou=0
  SD=np.zeros((map_size,map_size))
  for i in range (x-R,x+R+1):
    for j in range(y-R,y+R+1):
      if ((x-i)**2+(y-j)**2<=R*R):
        if 0<=i and i< map_size and 0<=j and j< map_size:
          #vamos simular que encontramos um obstaculo na posicao (i,j).
          #Na pratica nao sabemos (i,j).
          #Na pratica, teriamos os tempos obtidos dos sensores.
          #Com os tempos e angulos dos sensores, poderiamos estimar as posicoes
          if MR[i,j]==1:
            SD=SD+calc_prob(x,y,i,j)
            entrou=1
  if entrou:
    SD=normalize(SD)
  #vamos atualizar ME apenas na regiao de leitura do sensor
  for i in range (x-R,x+R+1):
    for j in range(y-R,y+R+1):
      if ((x-i)*(x-i)+(y-j)*(y-j)<=R*R):
        if 0<=i and i< map_size and 0<=j and j< map_size:
          ME[i,j]=SD[i,j]
  return ME

#faz a caminhada sequencial no grid
def walk2():
  #inicialmente são sabemos nada, entao vamos fixar a probabilidade em 1/2
  ME=(1/2)*np.ones((map_size,map_size))
  for i in range (0,map_size):
    for j in range(0,map_size):
      if MR[i,j] == 0:
        #Vamos fazer a medida num raio R
        ME=grade(i,j,ME)
  return ME
  
#normaliza o mapa
def normalize(M):
  maxi=np.max(M)
  mini=np.min(M)
  M=(M-mini)/(maxi-mini)
  return M

### - MAIN - ###
ME=walk2()
#ME=normalize(ME)
plt.matshow(ME);
plt.colorbar()
plt.gca().invert_yaxis()
plt.show()


