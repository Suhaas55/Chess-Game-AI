from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr


    """def calculateb(self,gametiles):
        value=0
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.tostring()=='P':
                        value=value-100

                    if gametiles[y][x].pieceonTile.tostring()=='N':
                        value=value-350

                    if gametiles[y][x].pieceonTile.tostring()=='B':
                        value=value-350

                    if gametiles[y][x].pieceonTile.tostring()=='R':
                        value=value-525

                    if gametiles[y][x].pieceonTile.tostring()=='Q':
                        value=value-1000

                    if gametiles[y][x].pieceonTile.tostring()=='K':
                        value=value-10000

                    if gametiles[y][x].pieceonTile.tostring()=='p':
                        value=value+100

                    if gametiles[y][x].pieceonTile.tostring()=='n':
                        value=value+350

                    if gametiles[y][x].pieceonTile.tostring()=='b':
                        value=value+350

                    if gametiles[y][x].pieceonTile.tostring()=='r':
                        value=value+525

                    if gametiles[y][x].pieceonTile.tostring()=='q':
                        value=value+1000

                    if gametiles[y][x].pieceonTile.tostring()=='k':
                        value=value+10000

        return value"""
    

    def calculateb(self,gametiles):
        # these tables basically define positional values for each piece type where the higher values indicate better positions for that particular piece

        #CHECK VALUES AGAIN FOR PIECE TABLE-READ ARTICLES ON BEST POSITIONS FOR EACH PIECE,ETC- DONT FORGET TO RECHECK FOR OPTIMAL TILES!!!-->delete comment later

        #pawns are valuable in the center and when advancing,adn also made row 6 negative for pawns movement who are in front of king
        p = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [9, 9, 9, 10, 10, 9, 9, 9],
            [2, 2, 4, 7, 7, 4, 2, 2],
            [1, 1, 2, 5.5, 5.5, 2, 1, 1],
            [0, 0, 0, 5, 5, 0, 0, 0],
            [1, -1, -2, 0, 0, -2, -1, 1],
            [1, 2, 2, -4, -4, 2, 2, 1],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        #knights better near center n poor at edges
        n = [
            [-10, -8, -6, -6, -6, -6, -8, -10],
            [-8, -4, 0, 0, 0, 0, -4, -8],
            [-6, 0, 2, 3, 3, 2, 0, -6],
            [-6, 1, 3, 4, 4, 3, 1, -6],
            [-6, 0, 3, 4, 4, 3, 0, -6],
            [-6, 1, 2, 3, 3, 2, 1, -6],
            [-9, -4, 0, 1, 1, 0, -4, -9],
            [-11, -8, -6, -6, -6, -6, -8, -11]
        ]
        #bishops netter in center basically for good diagonal control
        b = [
            [-4, -2, -2, -2, -2, -2, -2, -4],
            [-2, 0, 0, 0, 0, 0, 0, -2],
            [-2, 0, 1, 2, 2, 1, 0, -2],
            [-2, 1, 1, 2, 2, 1, 1, -2],
            [-2, 0, 2, 2, 2, 2, 0, -2],
            [-2, 2.5, 2, 2, 2, 2, 2.5, -2],
            [-2, 1, 0, 0, 0, 0, 1, -2],
            [-4, -2, -2, -2, -2, -2, -2, -4]
        ]
        #rook - 0 value for most positions n small penalty for corners
        r = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 2, 2, 2, 2, 2, 2, 1],
            [-1, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 0, 0, 0, 0, 0, -1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 0, 0, 0]
        ]
        #queens from central positions with safety,edghe bad overall kind of similar in all because nothing is too good and queen can be vulnerable if too free
        q = [
            [-4, -2, -2, -1, -1, -2, -2, -4],
            [-2, 0, 0, 0, 0, 0, 0, -2],
            [-2, 0, 1, 1, 1, 1, 0, -2],
            [-1, 0, 1, 1.5, 1.5, 1, 0, -1],
            [0, 0, 1, 1.5, 1.5, 1, 0, -1],
            [-2, 1, 1, 1, 1, 1, 1, -2],
            [-2, 0, 1, 0, 0, 0, 0, -2],
            [-4, -2, -2, -1, -1, -2, -2, -4]
        ]
        #center/opposite side position really bad so neg values corners/edges like castles good, better to staty behind pawn
        k = [
            [-6, -8, -8, -10, -10, -8, -8, -6],
            [-6, -8, -8, -10, -10, -8, -8, -6],
            [-6, -8, -8, -11, -11, -8, -8, -6],
            [-6, -8, -8, -10, -10, -8, -8, -6],
            [-4, -6, -6, -8, -8, -6, -6, -4],
            [-2, -4, -4, -4, -4, -4, -4, -2],
            [4, 4, 0, 0, 0, 0, 4, 4],
            [5, 6, 2, 0, 0, 2, 6, 5]
        ]

        
        value=0

        #going through entire board 64
        for x in range(8):
            for y in range(8):
                tile = gametiles[y][x]
                if tile.pieceonTile:
                    piece = tile.pieceonTile.tostring()
                    #checking if actuually a piece is there on tile but overall like starter code
                    if piece =='P': 
                        value -=100 + p[y][x]
                    elif piece =='N': 
                        value -=350 + n[y][x]
                    elif piece =='B': 
                        value -=350 + b[y][x]
                    elif piece =='R': 
                        value -=525 + r[y][x]
                    elif piece =='Q': 
                        value -=1000 + q[y][x]
                    elif piece =='K': 
                        value -=10000 + k[y][x]
                    elif piece =='p': 
                        value +=100 + p[y][x]
                    elif piece =='n': 
                        value +=350 + n[y][x]
                    elif piece =='b': 
                        value +=350 + b[y][x]
                    elif piece =='r': 
                        value +=525 + r[y][x]
                    elif piece =='q': 
                        value +=1000 + q[y][x]
                    elif piece == 'k': 
                        value +=10000 + k[y][x]
                    
                    #PAWNS ONLY
                    if piece.lower() =='p':
                        advancement_bonus = (y if piece == piece.lower() else 7 - y) * (8 - abs(x - 3.5))   #pushing for pawn advancement n promotion
                        value += advancement_bonus if piece.islower() else -advancement_bonus
                        #for pawns on the same horizontal
                        for i in range(y+1, 8):
                            if gametiles[i][x].pieceonTile and gametiles[i][x].pieceonTile.tostring().lower()=='p':
                                value -=30 if piece.islower() else 50
                                break

                    #For King safety--idea credit for ta for pawn too above
                    if piece.lower() =='k':
                        # Checkingg if there are pawns in front of the king for protection
                        for dy in [-1, 0, 1]:
                            if 0 <= y+dy < 8 and (not gametiles[y+dy][x].pieceonTile or gametiles[y+dy][x].pieceonTile.tostring().lower() !='p'):
                                value -=100 if piece.islower() else 100

                    #for castling
                    if piece == 'K' and (x, y) == (4, 7):  # White side
                    #if the castling is still possible
                        kingside_clear = all(not gametiles[7][i].pieceonTile for i in [5, 6])
                        queenside_clear = all(not gametiles[7][i].pieceonTile for i in [1, 2, 3])
    
                        if kingside_clear or queenside_clear:
                            value -= 40  #bonus if castling is there but not yet castled-so potential is there incase check is made or something

                    elif piece == 'k' and (x, y) == (4, 0):  # Black side
                        kingside_clear = all(not gametiles[0][i].pieceonTile for i in [5, 6])
                        queenside_clear = all(not gametiles[0][i].pieceonTile for i in [1, 2, 3])
    
                        if kingside_clear or queenside_clear:
                            value += 40

        return value
    


    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
