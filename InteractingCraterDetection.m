function varargout = InteractingCraterDetection(varargin)
% INTERACTINGCRATERDETECTION M-file for InteractingCraterDetection.fig
%      INTERACTINGCRATERDETECTION, by itself, creates a new INTERACTINGCRATERDETECTION or raises the existing
%      singleton*.
%
%      H = INTERACTINGCRATERDETECTION returns the handle to a new INTERACTINGCRATERDETECTION or the handle to
%      the existing singleton*.
%
%      INTERACTINGCRATERDETECTION('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in INTERACTINGCRATERDETECTION.M with the given input arguments.
%
%      INTERACTINGCRATERDETECTION('Property','Value',...) creates a new INTERACTINGCRATERDETECTION or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before InteractingCraterDetection_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to InteractingCraterDetection_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help InteractingCraterDetection

% Last Modified by GUIDE v2.5 26-Feb-2014 13:37:45

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @InteractingCraterDetection_OpeningFcn, ...
    'gui_OutputFcn',  @InteractingCraterDetection_OutputFcn, ...
    'gui_LayoutFcn',  [] , ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before InteractingCraterDetection is made visible.
function InteractingCraterDetection_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to InteractingCraterDetection (see VARARGIN)

% Choose default command line output for InteractingCraterDetection
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes InteractingCraterDetection wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = InteractingCraterDetection_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in btn_input.
function btn_input_Callback(hObject, eventdata, handles)
% hObject    handle to btn_input (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global dem_head
global dem
t1=clock;
[filename,pathname]=uigetfile(...\
    {'*.txt','txt-files(*.txt)';'*.*','All-files(*.*)'},'Open:','');
fullpath=fullfile(pathname,filename);
if isequal(filename,0) || isequal(pathname,0)
    return;
else
    file=fullpath;
    [dem,dem_head,dem_img]=readAscii(file);
    % dem information
    % ncols         1452
    % nrows         1378
    % xllcorner     5689950.6739785
    % yllcorner     3307559.3275701
    % cellsize      499.542418
    % NODATA_value  -9999
    for i=1:6
        len_head(i)=size(num2str(dem_head(i)),2);
    end
    set(handles.text_dem,'String',...
        ['DEM Info:' blanks(max(len_head)-size('DEM Info:',2)+14);...
        ['ncols         ' num2str(dem_head(1)) blanks(max(len_head)-len_head(1))];...
        ['nrows         ' num2str(dem_head(2)) blanks(max(len_head)-len_head(2))];...
        ['xllcorner     ' num2str(dem_head(3)) blanks(max(len_head)-len_head(3))];...
        ['yllcorner     ' num2str(dem_head(4)) blanks(max(len_head)-len_head(4))];...
        ['cellsize      ' num2str(dem_head(5)) blanks(max(len_head)-len_head(5))];...
        ['NODATA_value  ' num2str(dem_head(6)) blanks(max(len_head)-len_head(6))]]);
    % dem image
    axes(handles.axes_Image);
    imshow(dem_img);
    
    % clear table
    cur_data = get(handles.table_statistics,'data');
    [data_row,data_col] = size(cur_data)
    if data_row>0
        cur_data(1,:)=[];
        set(handles.table_statistics, 'data', cur_data);
    end
end
% 'Time cost:'
set(handles.text_costtiime,'String',['Time cost: ',num2str(etime(clock,t1))]);


% --- Executes on mouse press over figure background, over a disabled or
% --- inactive control, or over an axes background.
function figure1_WindowButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global dem_head
global isClicked
if numel(dem_head)>0
    % global firstpt
    
    % isClicked=1;
    % firstpt = get(gca, 'CurrentPoint');
    % x = firstpt(1,1);
    % y = firstpt(1,2);
    
    [click_x,click_y]=ginput(2);
    select_xy=sort([click_x,click_y],1);
    select_xy(select_xy<0)=0;
    select_xy=ceil(select_xy);
    sx=select_xy(:,1);
    sy=select_xy(:,2);
    sx(sx>dem_head(1))=dem_head(1);
    sy(sy>dem_head(2))=dem_head(2);
    select_xy=[sx,sy];
    % insert into table
    % initialize table: workspace中创建数组a=[1:5],table-data指定为a
    cur_data = get(handles.table_statistics,'data');
    [data_row,data_col] = size(cur_data);
    rec_id=data_row-1+1;
    insert_data={rec_id,[num2str(select_xy(1,1)) ',' num2str(select_xy(1,2))],...
        [num2str(select_xy(2,1)) ',' num2str(select_xy(2,2))],...
        abs(select_xy(1,1)-select_xy(2,1)),abs(select_xy(1,2)-select_xy(2,2))};
    cur_data(data_row+1,1:5) = insert_data;
    set(handles.table_statistics, 'data', cur_data);
    % draw rectangle
    rectangle('Position',[select_xy(1,1),select_xy(1,2),...
        select_xy(2,1)-select_xy(1,1),select_xy(2,2)-select_xy(1,2)],...
        'EdgeColor','r','LineWidth',2);
    line(click_x,click_y);
    % mark rectangle id
    text(select_xy(1,1)+10,select_xy(1,2)+10,['ID = ' num2str(rec_id)]);
    
end

% --- Executes on button press in btn_exit.
function btn_exit_Callback(hObject, eventdata, handles)
% hObject    handle to btn_exit (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
clc;
clear all;
close;


% --- Executes on mouse motion over figure - except title and menu.
function figure1_WindowButtonMotionFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% % handles    structure with handles and user data (see GUIDATA)
% global isClicked
% global firstpt
% global secondpt
% if isClicked==1
%     secondpt = get(gca, 'CurrentPoint');
%     xy=sort([secondpt(1,:);firstpt(1,:)],1)
%     rectangle('Position',[xy(1,1),xy(1,2),...
%         xy(2,1)-xy(1,1),xy(2,2)-xy(1,2)],'EdgeColor','r','LineWidth',2);
% end

% --- Executes on mouse press over figure background, over a disabled or
% --- inactive control, or over an axes background.
function figure1_WindowButtonUpFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% global isClicked
% global firstpt
% global secondpt
% xy=sort([secondpt(1,:);firstpt(1,:)],1)
% rectangle('Position',[xy(1,1),xy(1,2),...
%         xy(2,1)-xy(1,1),xy(2,2)-xy(1,2)],'EdgeColor','r','LineWidth',2);
% isClicked=0;


% --- Executes on button press in btn_process.
function btn_process_Callback(hObject, eventdata, handles)
% hObject    handle to btn_process (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global dem_head
global dem

if numel(dem_head)>0
    rect = get(handles.table_statistics,'data');
    if size(rect,1)<1
        msgbox('Please select a region for calculation!');
    else
        files4python=[];
        t1=clock;
        for i=1:size(rect,1)
            ncols=rect(i,4);ncols=ncols{1};
            nrows=rect(i,5);nrows=nrows{1};
            %left-up: x
            cor_pt=rect(i,2);
            cor_pt=cor_pt{1};
            comma_index=find(cor_pt==',');
            cor_x=dem_head(3)+str2num(cor_pt(1:comma_index-1))*dem_head(5);
            %left-bottom: y
            cor_pt=rect(i,3);
            cor_pt=cor_pt{1};
            comma_index=find(cor_pt==',');
            cor_y=dem_head(4)+(dem_head(2)-str2num(cor_pt(comma_index+1:end)))*dem_head(5);
            
            head=[ncols;nrows;cor_x;cor_y;dem_head(5);dem_head(6)];
            if isdir('select')==0
                mkdir('select');
            end
            path=['select/r0_' num2str(ncols) 'x' num2str(nrows) '.txt'];
            exist_id=0;
            while(exist(path))
                exist_id=exist_id+1;
                path=['select/r' num2str(exist_id) '_' num2str(ncols) 'x' num2str(nrows) '.txt'];
            end
            cor_pt=rect(i,2);
            cor_pt=cor_pt{1};
            start_x=str2num(cor_pt(1:comma_index-1));
            start_y=str2num(cor_pt(comma_index+1:end));
            [num_row,num_col]=size(dem);
            if start_x==0
                start_x=1;
            end
            if start_y==0
                start_y=1;
            end
            end_x=start_x+ncols-1;
            if start_x+ncols>num_col
                end_x=num_col;
            end
            end_y=start_y+nrows-1;
            if start_y+nrows>num_row
                end_y=num_row;
            end
            writeAscii(dem(start_y:end_y,start_x:end_x),head,path);
            
            files4python=[files4python ' ' path];
        end
        % python execution
        files4python=files4python(2:end);
        [result,status] = python('map.py ',files4python);
        msgbox([{'Extraction is finished.'};{result}]);
        
        %% get file path of raster and plg
        info_index=find(result=='[');
        warning_info=result(1:info_index(1)-1);
        costtime_info=result(info_index(1)+1:info_index(2)-3);%[...]
        data_info=result(info_index(2)+1:end-2);%[...]
        %
        cf_index=find(costtime_info==' ');
        cost_time=costtime_info(cf_index(3)+1:cf_index(4)-1);
        disp(['Python cost time: ' cost_time]);
        %
        %raster_path={};
        dfb_index=find(data_info==',');
        %'data raster plg'
        
        % 'Time cost:'
        set(handles.text_costtiime,'String',['Time cost: ',num2str(etime(clock,t1))]);
    end
else
    msgbox('Please input DEM!');
end
