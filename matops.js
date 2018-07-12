function convolve(mat, kern){
    var kh = kern.length, kw = kern[0].length;
    var khh = Math.floor(kh/2), khw = Math.floor(kw/2);    
    var mh = mat.length, mw = mat[0].length;
    
    out = new Array(mh);
    for(var j = 0; j < mh; j++){
        out[j] = new Array(mw);
        for(var i = 0; i < mw; i++){
        
            var sum = 0;
            for(var y = 0; y < kh; y++){
                for(var x = 0; x < kw; x++){
                    var r = Math.max(0, Math.min(mh-1, j-khh+y));
                    var c = Math.max(0, Math.min(mw-1, i-khw+x));
                    sum += kern[y][x]*mat[r][c];
                }
            }
            out[j][i] = sum;
        }
    }
    return out;
}


function rgbaToMat(c){
    var ctx = c.getContext("2d");
    var raw = ctx.getImageData(0,0,320,240);
    m = new Array(240);
    for(var j = 0; j < 240; j++){
        m[j] = new Array(320);
        var row = j*320;
        
        for(var i = 0; i < 320; i++){
            var col = i*4;
            
            m[j][i] = Math.floor((raw[row+col]+         // r
                                raw[row+col+1]+         // g
                                raw[row+col+2])/3);     // b
        }
    }
}

function preloadImageFromURL(url){
    var image = new Image();
    image.onload = function(){ ctx.drawImage(image, 0, 0); };
    image.src = url;
    
    return image;
}

