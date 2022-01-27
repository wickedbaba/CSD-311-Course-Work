#include <iostream>
#include <vector>
#include <algorithm>
#include <math.h>
using namespace std;

// global variables
int n = 3;

// 3x3x3 vectors - Initialized with Zero
vector<vector<vector<int> > >  magicCube(n, vector< vector<int> > (n, vector<int> (n, 0)));
vector<vector<vector<int> > >  gameBoard(n, vector< vector<int> > (n, vector<int> (n, 0)));
int magicConstant = (n*(pow(n,3)+1))/2;

// vector to track which values are already used - default flase
vector<bool> usedSpaces(pow(n,3) + 1 , false);
int scoreComp, scoreHuman;

// a structure of Point which holds i, j, k coordinates
struct Point{
    int i,j,k;
};

// vector of Moves 
vector<Point> userMoves, computerMoves;

// utility to print magic Cube
void printCube(){
    for(int i=0; i<n ;i++){
        for(int j=0; j<n; j++){
            cout<<endl;
            for(int k=0 ;k<n;k++){
                cout<<magicCube[i][j][k]<<' ';
            }
        }
        cout<<endl;
    }
}

// utility to render the game board
void drawGameBoard(){
    for(int i=0; i<n ;i++){
        for(int j=0 ; j<n ;j++){
            cout<<endl;
            for(int k=0 ; k<n ; k++){
                cout<<'('<<i<<','<<j<<','<<k<<") ";
            }
        }
        cout<<endl;
    }
    cout<<endl;
        for(int i=0; i<n ;i++){
        for(int j=0 ; j<n ;j++){
            cout<<endl;
            for(int k=0 ; k<n ; k++){
                // 0 - empty
                // 1 - X
                // 2 - O
                if(gameBoard[i][j][k] == 0) cout<<"- ";
                else if(gameBoard[i][j][k] == 1) cout<<"\033[1;32mX\033[0m ";
                else if(gameBoard[i][j][k] == 2) cout<<"\033[1;34mO\033[0m ";
            }
        }
        cout<<endl;
    }
}

// return i,j,k co-ordiantes of a number in magic cube
Point valueToCoordinate(int x){
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            for (int k = 0; k < n; k++){
                if (magicCube[i][j][k] == x)
                    return {i, j, k};
            }
        }
    }
}

// helper function to get the value of magic cube @ i, j ,k coordinates
int coordinateToValue(int i, int j, int k){   
    i++,j++,k++;
    int a = (i - j + k - 1) % n;
    int b = (i - j - k) % n;
    int c = (i + j + k - 2) % n;

    a = a < 0 ? a + 3 : a;
    b = b < 0 ? b + 3 : b;
    c = c < 0 ? c + 3 : c;

    return a * 9 + b * 3 + c + 1 ;
}

// utility to generate the magic cube 
void makeMagicCube(){
    for(int i = 0 ; i<n ; i++){
        for(int j = 0 ; j <n ; j++){
            for(int k = 0; k <n ; k++){
                
                magicCube[i][j][k] = coordinateToValue(i,j,k); 
            }
        }
    }    
}

// take input from user in form of co-ordinates
bool moveByUser(){
    cout<<"\nUser Move - ";
    cout<<"\nEnter Co-ordinates "<<n<<" spaced integers: ";
    Point p;
    cin>>p.i>>p.j>>p.k;
    if(!usedSpaces[magicCube[p.i][p.j][p.k]]){
        gameBoard[p.i][p.j][p.k] = 1;
        usedSpaces[magicCube[p.i][p.j][p.k]] = true;
        userMoves.push_back(p);
        // user completed the move, so userMove is now false
        return false;
    }
    else{
        cout<<"\n\033[1;31mSpace filled please choose another place.\033[0m";
        return true;
    }
}


// utlity to check if space is left or not 
bool spaceLeft(){
    for(int i = 1 ; i <= pow(n,3) ; i++){
        if(usedSpaces[i] == 0)
            return true;
    }
    return false;
}

// Utilty to display moves of users and computer
void showMoves(){
    cout<<"User Moves: ";
    for(auto p: userMoves){
        cout<<magicCube[p.i][p.j][p.k]<<", ";        
    }

    cout<<endl;

    cout<<"Computer Moves: ";
    for(auto p: computerMoves){
        cout<<magicCube[p.i][p.j][p.k]<<", ";        
    }
}

// calculate distance between two points in 3D space
double distance(Point p1, Point p2){
    int x = pow(p1.i-p2.i, 2);
    int y = pow(p1.j-p2.j, 2);
    int z = pow(p1.k-p2.k, 2);
    return pow(x+y+z, 0.5);
}

// check if 3 point in 3D space are collinear or not
bool isCollinear(Point p1, Point p2, Point p3){
    // p1p2+p2p3 = p1p3
    double p1p2 = distance(p1,p2);
    double p2p3 = distance(p2,p3);
    double p1p3 = distance(p1,p3);
    vector<double> lengths({p1p2, p2p3, p1p3});
    sort(lengths.begin(), lengths.end());
    return lengths[0] + lengths[1] == lengths[2];
}

// when computer can neither win nor block users winning move then it plays suitable random move 
Point make_2() {
    // centers preffered
    if(!usedSpaces[magicCube[1][1][1]])
        return {1,1,1};
    else if(!usedSpaces[magicCube[1][0][1]])
        return {1,0,1};    
    else if(!usedSpaces[magicCube[1][1][2]])
        return {1,1,2};
    else if(!usedSpaces[magicCube[1][2][1]])
        return {1,2,1};
    else if(!usedSpaces[magicCube[1][1][0]])
        return {1,1,0};
    else if(!usedSpaces[magicCube[0][1][1]])
        return {0,1,1};
    else if(!usedSpaces[magicCube[2][1][1]])
        return {2,1,1};

    // non-corners
    else if(!usedSpaces[magicCube[0][0][2]])
        return {0,0,2};
    else if(!usedSpaces[magicCube[0][2][2]])
        return {0,2,2};
    else if(!usedSpaces[magicCube[0][2][0]])
        return {0,2,0};
    else if(!usedSpaces[magicCube[2][0][0]])
        return {2,0,0};
    else if(!usedSpaces[magicCube[2][0][2]])
        return {2,0,2};
    else if(!usedSpaces[magicCube[2][2][2]])
        return {2,2,2};
    else if(!usedSpaces[magicCube[2][2][0]])
        return {2,2,0};
    else if(!usedSpaces[magicCube[0][0][0]])
        return {0,0,0};
    else if(!usedSpaces[magicCube[0][0][1]])
        return {0,0,1};
    else if(!usedSpaces[magicCube[0][1][0]])
        return {0,1,0};
    else if(!usedSpaces[magicCube[0][2][1]])
        return {0,2,1};
    else if(!usedSpaces[magicCube[0][1][2]])
        return {0,1,2};
    else if(!usedSpaces[magicCube[2][0][1]])
        return {2,0,1};
    else if(!usedSpaces[magicCube[2][1][0]])
        return {2,1,0};
    else if(!usedSpaces[magicCube[2][2][1]])
        return {2,2,1};
    else if(!usedSpaces[magicCube[2][1][2]])
        return {2,1,2};
    else
    {
        for(int i=1;i<=pow(n,3);i++){
            if(!usedSpaces[i]){
                return valueToCoordinate(i);
            }
        }
    }
}

// utilty for AI to decide next move
Point possibleWin(){ 
    int sizeC = computerMoves.empty() ? 0 : computerMoves.size();
    int sizeH = userMoves.empty() ? 0 : userMoves.size();
    // wining condition checker for AI
    for (int i = 0; i < sizeC - 1; i++){
        for (int j = i + 1; j < sizeC ; j++){
            Point p1 = computerMoves[i];
            Point p2 = computerMoves[j];
            int a = magicCube[p1.i][p1.j][p1.k];
            int b = magicCube[p2.i][p2.j][p2.k];
            int c = magicConstant - (a + b);
            if ((c>0 && c<28) && !usedSpaces[c]){
                // collinear
                Point p3 = valueToCoordinate(c);
                if (isCollinear(p1, p2, p3)){
                    return p3;
                }
            }
        }
    }

    // winning condition for human, if found then this position will be blocked by the AI
    for (int i = 0; i < sizeH - 1; i++){
        for (int j = i + 1; j < sizeH ; j++){
            Point p1 = userMoves[i];
            Point p2 = userMoves[j];
            int a = magicCube[p1.i][p1.j][p1.k];
            int b = magicCube[p2.i][p2.j][p2.k];
            int c = magicConstant - (a + b);
            if ((c>0 && c<28) && !usedSpaces[c]){
                Point p3 = valueToCoordinate(c);
                if (isCollinear(p1, p2, p3)){
                    return p3;
                }
            }
        }
    }
    // make a random move
   return make_2();
}

// method for AI to make a move
bool moveByAI(){
    Point p = possibleWin();
    gameBoard[p.i][p.j][p.k] = 2;
    usedSpaces[magicCube[p.i][p.j][p.k]] = true;
    computerMoves.push_back(p);
    return true;
}

// Calcluate the score of Human and the Computer
void scoreBoard(){
    scoreComp = 0, scoreHuman = 0;  
    int sizeC = computerMoves.empty() ? 0 : computerMoves.size();
    int sizeH = userMoves.empty() ? 0 : userMoves.size();
    
    // this nested loop checks for triplets in computer number array which satisfy all required conditions
    for(int i = 0 ; i < sizeC - 2 ; i++){
        for(int j = i+1 ; j < sizeC - 1 ; j++){
            for(int k = j+1 ; k < sizeC ; k++){
                Point p1 = computerMoves[i];
                Point p2 = computerMoves[j];
                Point p3 = computerMoves[k];
                // sums and compares all the given triplets to 42
                if ((magicCube[p1.i][p1.j][p1.k] + magicCube[p2.i][p2.j][p2.k]+ magicCube[p3.i][p3.j][p3.k] == magicConstant) && isCollinear(p1, p2, p3)){
                    scoreComp++;
                }
            }
        }
    }

    // this nested loop checks for triplets in user number array which satisfy all required conditions
    for(int i = 0 ; i < sizeH - 2 ; i++){
        for(int j = i+1 ; j < sizeH - 1 ; j++){
            for(int k = j+1 ; k < sizeH ; k++){
                Point p1 = userMoves[i];
                Point p2 = userMoves[j];
                Point p3 = userMoves[k];
                // sums and compares all the given triplets to 42
                if ((magicCube[p1.i][p1.j][p1.k] + magicCube[p2.i][p2.j][p2.k]+ magicCube[p3.i][p3.j][p3.k] == magicConstant) && isCollinear(p1, p2, p3)){
                    scoreHuman++;
                }
            }
        }
    }
    // outputs the score of human and computer
    cout<<"\n\033[1;33mScore - Human: "<<scoreHuman<<" Computer: "<<scoreComp<<"\033[0m";
    // output the move made by the computer
    if(sizeC > 0) {
        Point p = computerMoves[sizeC-1]; 
        cout<<"\nComputer's last move: "<<'('<<p.i<<','<<p.j<<','<<p.k<<") ";
    }
}

// main method
int main(){
    cout << "Generating Magic Cube\n";
    makeMagicCube(); // it starts by making a 3 x 3 x 3 magic cube and displaying it 
    printCube();

    char choice;
    // Then it asks for choice from the user, the choices being - 
    // Would the user play first OR Would the computer play first
    do{
        cout << "Do you want to play first? (y/n)  ";
        cin >> choice;
        choice = tolower(choice);
        if (choice != 'y' && choice != 'n')
            cout << "Enter a valid Choice\n";
    } while (choice != 'y' && choice != 'n');
    // Then we declare and use two variables, which would help us in running the program from start till the end conditions
    // userMove - stores the user preference
    // gameLoop - controls how long the loop will run  

    bool userMove, gameLoop = true;
    if (choice == 'y') userMove = true;
    do{
        drawGameBoard(); // this function helps us in drawing the coordinate board, which is referenced by the user to play the game 
        showMoves(); // this function shows the  3x3x3 grid where the X and O are being placed
        scoreBoard(); // this functions displays the score board

        // breaks the loop if win limit is reached
        if (scoreComp >= 10 || scoreHuman >= 10) break;

        // if true - the User plays first // else Computer plays first
        if (userMove) 
            userMove = moveByUser(); // this function helps in inputing and placing the user commands
        else 
            userMove = moveByAI(); // this function asks the AI to play its turn 

        // this function checks if any space is left in teh 3x3x3 Grid 
        // if no space is left, this is puts gameLoop = false, which helps in exiting the loop
        if(!spaceLeft()) 
            gameLoop = false;
    }while(gameLoop);

    drawGameBoard();
    showMoves();
    scoreBoard();
    if(scoreComp > scoreHuman) cout<<"\n\033[1;32mComputer Wins\033[0m\n";
    else if (scoreComp == scoreHuman) cout << "\n\033[1;32mThe Match Ends In Draw\033[0m\n";
    else cout<<"\n\033[1;32mHuman Wins\033[0m\n";
    return 0;
}