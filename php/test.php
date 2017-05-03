<?php

function sendInfoToPythonServer($str)
{
	$address = '127.0.0.1';
	$port = 45102;
	
	$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
	$result = socket_connect($socket, $address, $port);
	socket_write($socket, $str, strlen($str));
    	
	socket_close($socket);
}


if ($_SERVER['REQUEST_METHOD']=="GET")
{

    $echoStr = $_GET["echostr"];
    echo $echoStr;
    
    
    $myfile = fopen("a.txt","w");
    fwrite($myfile, $echoStr);
    fclose($myfile);

    exit;

}
else if ($_SERVER['REQUEST_METHOD']=="POST")
{
    //$postStr = $GLOBALS["HTTP_RAW_POST_DATA"];
    $postStr = file_get_contents("php://input"); 
  

	if (!empty($postStr)){
		$postObj = simplexml_load_string($postStr, 'SimpleXMLElement', LIBXML_NOCDATA); 
		$fromUsername = $postObj->FromUserName; 
		$toUsername = $postObj->ToUserName; 
		$keyword = trim($postObj->Content); 
		$time = time(); 
		$textTpl = "<xml> 
		<ToUserName><![CDATA[%s]]></ToUserName> 
		<FromUserName><![CDATA[%s]]></FromUserName> 
		<CreateTime>%s</CreateTime> 
		<MsgType><![CDATA[text]]></MsgType> 
		<Content><![CDATA[%s]]></Content> 
		<FuncFlag>0<FuncFlag> 
		</xml>"; 
    	if(!empty( $keyword )){
            $contentStr = $keyword;
			
			sendInfoToPythonServer($contentStr);

			$resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, $contentStr); 
			echo $resultStr; 
		}
	}
}



?>

