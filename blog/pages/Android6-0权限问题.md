title: Android6.0权限问题
date: 2015-11-09 09:06:32
tags: [Android,api23,权限,permission]

## 6.0权限问题
* 1.Android6.0的权限与以往不同。
	Android6.0之后引入了新的权限机制，不再是安装时就申请权限，获得后用户不可修改。6.0以后安装时不申请权限，而是运行时申请权限，而且用户可以随时到设置里撤消或允许权限。当然如果程序员不知道这回事就把需要权限的项目的targetSdkVersion的值改为23以下，这样6.0会以原来的方式对待这个软件。如果不改的话，在运行需要权限的代码时会FC，也可以手动到设置里赋予权限但是这个不合适用户使用。
``` xml
	<uses-sdk
		android:minSdkVersion="8"
		android:targetSdkVersion="23" />
```
* 2.解决方法
还是要在AndroidManifest.xml添加权限
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
用下面的代码获取是否获取到权限。
``` java
int hasWriteContactsPermission = checkSelfPermission(Manifest.permission.权限常量);
//获得权限的状态码。如果为PackageManager.PERMISSION_GRANTED就是已获得权限。
```
然后用下面代码申请权限
``` java
final int REQUEST_CODE_ASK_PERMISSIONS = 123;
//标记数字
requestPermissions(new String[] {Manifest.permission.权限常量}, 
			REQUEST_CODE_ASK_PERMISSIONS);
```
试着做了一个单权限申请的方法
``` java
/**
* 6.0的权限申请传入权限常量如果获取到了返回true，否则异步申请权限，返回false。
* @param permissionStr 权限常量字符串
* @return 如果获取到了返回true，否则异步申请权限，返回false。
*
*/
final int REQUEST_CODE_ASK_PERMISSIONS = 123;
private boolean insertDummyContactWrapper(String permissionStr) { 
//标记数字(onRequestPermissionsResult方法中的requestCode)
int hasWriteContactsPermission = checkSelfPermission(permissionStr);
//获得权限的状态码。如果为PackageManager.PERMISSION_GRANTED就是已获得权限。
if (hasWriteContactsPermission != PackageManager.PERMISSION_GRANTED) {
	//打印吐司提示未获取权限，如果没有弹出申请权限窗口请到设置中允许权限。
	requestPermissions(new String[] {permissionStr}, 
			REQUEST_CODE_ASK_PERMISSIONS); 
	return false; 
	} 
	return true;
} 
```
不论获取到权限没有都会回调Activity的onRequestPermissionsResult方法。
``` java
/**
*
*@param requestCode 调用requestPermissions时设置的标记数字。
*@param permissions 请求的权限字符串常量数组。
*@param grantResults 与permissions数组对应的权限的状态码为PackageManager.PERMISSION_GRANTED就说明申请成功。
*/
public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults){
	if(requestCode==REQUEST_CODE_ASK_PERMISSIONS){
	for(int i=0;i<permissions.length;i++){
		if(grantResults[i]==PackageManager.PERMISSION_GRANTED){
			Toast.makeText(MainActivity.this, permissions[i]+"获取成功", Toast.LENGTH_SHORT)
				.show();
		}else{
			Toast.makeText(MainActivity.this, permissions[i]+"获取失败", Toast.LENGTH_SHORT)
				.show();
		}
	}
	}else{
		super.onRequestPermissionsResult(requestCode, permissions, grantResults);
	}
}
```
	以上的方法checkSelfPermission和requestPermissions都是api23(6.0)后Activity的。如果要兼容需要判断版本。
``` java
if (Build.VERSION.SDK_INT >= 23) { 
	// Marshmallow+ 
} else { 
	// Pre-Marshmallow 
} 
```
我建议用v4兼容库，已对这个做过兼容，用这个方法代替：

* ContextCompat.checkSelfPermission()
被授权函数返回PERMISSION_GRANTED，否则返回PERMISSION_DENIED ，在所有版本都是如此。

* ActivityCompat.requestPermissions()
这个方法在M之前版本调用，OnRequestPermissionsResultCallback 直接被调用，带着正确的 PERMISSION_GRANTED或者PERMISSION_DENIED 。

* ActivityCompat.shouldShowRequestPermissionRationale()
在M之前版本调用，永远返回false。在M版时弹出一次申请框后为true。

用v4包的这三方法，完美兼容所有版本！这个方法需要额外的参数，Context or Activity。别的就没啥特别的了。
或是用V13 的FragmentCompat.requestPermissions() FragmentCompat.shouldShowRequestPermissionRationale();
更多更详细的看[Android M 新的运行时权限开发者需要知道的一切](http://www.jianshu.com/p/e1ab1a179fbb)