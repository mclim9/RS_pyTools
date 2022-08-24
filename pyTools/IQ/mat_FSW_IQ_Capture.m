    fprintf(fsw,'FORM REAL,32');
    fprintf(fsw,'TRAC:IQ:DATA:FORM IQP');

    %##############################################################
    %### MAKE MEASUREMENT!!!!!!!!!!!!!!!!!!!!!!!!
    %##############################################################
    fprintf(fsw,':INIT:IMM;*OPC?');
    fscanf(fsw);
    B.ErrorDescription = check_for_error(B.Comm);

    %##############################################################
    %### Read IQ Data
    %##############################################################
    fprintf(fsw,'TRAC:IQ:DATA:MEMORY?');
    fread(fsw,1);

    a = str2num(char(fread(fsw,1)'));
    nTotalBytes = str2num(char(fread(fsw,a)'));
    nReads = ceil(nTotalBytes/nMaxBlockSize);
    nReadBytes = nMaxBlockSize;
    nLeftBytes = nTotalBytes;
    tracH=[];
    for nReadCnt=1:nReads
        if nLeftBytes < nReadBytes
            nReadBytes = nLeftBytes;
        end
        tracH = [tracH;fread(fsw, nReadBytes)]; %#ok<*AGROW>
        nLeftBytes = nLeftBytes - nReadBytes;
    end
    nValues = nTotalBytes/8;
    fread(fsw,1);
    %End read


    %##############################################################
    %### Convert IQ Data to Matlab format
    %##############################################################
    % Reshape data, so I is one column and Q the other
    % IQIQ: 1D Array, Interleaved I&Q
    %   IQ: 2D Array, I & Q in separate columns
    IQIQ = typecast(uint8(tracH(1:nTotalBytes)), 'single');
    IQ = reshape(IQIQ', 2, nValues)';
    IQ = double(IQ);
    Y = complex(IQ(:,1),IQ(:,2));                                       %#ok<NASGU>
    XDelta = 1/(B.Fs*1e6);                                              %#ok<NASGU>
    save([outputFilename '_' num2str(B.Fs) 'MHz.mat'], 'Y','XDelta');   %Save IQ samples in '.mat' format

    D.IQdata = IQIQ; %MMM Added for Qualcomm