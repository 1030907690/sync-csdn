---
layout:					post
title:					"Spring Security loadUserByUsername传递多个参数"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
@[TOC](目录)
## 前言
- 我们使用Spring Security做登录，一般来说都要实现`UserDetailsService`接口，代码如下。

```java
public interface UserDetailsService {
	UserDetails loadUserByUsername(String username) throws UsernameNotFoundException;
}

```
- 是的，`loadUserByUsername`方法仅有一个`username`参数，如果我们是做SaaS平台，多渠道登录，名称允许重复的话，这可怎么玩儿。
- 下面提供2种方法。
## 自定义一个DaoAuthenticationProvider
- 新建`CustomerDaoAuthenticationProvider.java`，其实是把`DaoAuthenticationProvider`代码抄下来，修改了`userDetailsService`和`UserDetails loadedUser = this.getUserDetailsService().loadUserByUsername(username, authentication.getDetails());`。把`UsernamePasswordAuthenticationToken`的`details`属性作为扩展参数传入新的`loadUserByUsername`方法。
```
 
import com.works.framework.web.WebUserDetailsServiceImpl;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.InternalAuthenticationServiceException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.authentication.dao.AbstractUserDetailsAuthenticationProvider;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsPasswordService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.factory.PasswordEncoderFactories;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.util.Assert;

/**
 * @author Zhou Zhongqing
 * @ClassName CustomerDaoAuthenticationProvider.java
 * @description: TODO
 * @date 2022-08-11 17:33
 */
public class CustomerDaoAuthenticationProvider extends AbstractUserDetailsAuthenticationProvider {

 
    private static final String USER_NOT_FOUND_PASSWORD = "userNotFoundPassword";

    private PasswordEncoder passwordEncoder;
 
    private volatile String userNotFoundEncodedPassword;

    private WebUserDetailsServiceImpl userDetailsService;

    private UserDetailsPasswordService userDetailsPasswordService;

    public CustomerDaoAuthenticationProvider() {
        setPasswordEncoder(PasswordEncoderFactories.createDelegatingPasswordEncoder());
    }

    @Override
    @SuppressWarnings("deprecation")
    protected void additionalAuthenticationChecks(UserDetails userDetails,
                                                  UsernamePasswordAuthenticationToken authentication) throws AuthenticationException {
        if (authentication.getCredentials() == null) {
            this.logger.debug("Failed to authenticate since no credentials provided");
            throw new BadCredentialsException(this.messages
                    .getMessage("AbstractUserDetailsAuthenticationProvider.badCredentials", "Bad credentials"));
        }
        String presentedPassword = authentication.getCredentials().toString();
        if (!this.passwordEncoder.matches(presentedPassword, userDetails.getPassword())) {
            this.logger.debug("Failed to authenticate since password does not match stored value");
            throw new BadCredentialsException(this.messages
                    .getMessage("AbstractUserDetailsAuthenticationProvider.badCredentials", "Bad credentials"));
        }
    }

    @Override
    protected void doAfterPropertiesSet() {
        Assert.notNull(this.userDetailsService, "A UserDetailsService must be set");
    }

    @Override
    protected UserDetails retrieveUser(String username, UsernamePasswordAuthenticationToken authentication)
            throws AuthenticationException {
        prepareTimingAttackProtection();
        try {
            UserDetails loadedUser = this.getUserDetailsService().loadUserByUsername(username, authentication.getDetails());
            if (loadedUser == null) {
                throw new InternalAuthenticationServiceException(
                        "UserDetailsService returned null, which is an interface contract violation");
            }
            return loadedUser;
        } catch (UsernameNotFoundException ex) {
            mitigateAgainstTimingAttack(authentication);
            throw ex;
        } catch (InternalAuthenticationServiceException ex) {
            throw ex;
        } catch (Exception ex) {
            throw new InternalAuthenticationServiceException(ex.getMessage(), ex);
        }
    }

    @Override
    protected Authentication createSuccessAuthentication(Object principal, Authentication authentication,
                                                         UserDetails user) {
        boolean upgradeEncoding = this.userDetailsPasswordService != null
                && this.passwordEncoder.upgradeEncoding(user.getPassword());
        if (upgradeEncoding) {
            String presentedPassword = authentication.getCredentials().toString();
            String newPassword = this.passwordEncoder.encode(presentedPassword);
            user = this.userDetailsPasswordService.updatePassword(user, newPassword);
        }
        return super.createSuccessAuthentication(principal, authentication, user);
    }

    private void prepareTimingAttackProtection() {
        if (this.userNotFoundEncodedPassword == null) {
            this.userNotFoundEncodedPassword = this.passwordEncoder.encode(USER_NOT_FOUND_PASSWORD);
        }
    }

    private void mitigateAgainstTimingAttack(UsernamePasswordAuthenticationToken authentication) {
        if (authentication.getCredentials() != null) {
            String presentedPassword = authentication.getCredentials().toString();
            this.passwordEncoder.matches(presentedPassword, this.userNotFoundEncodedPassword);
        }
    }

    /**
     * Sets the PasswordEncoder instance to be used to encode and validate passwords. If
     * not set, the password will be compared using
     * {@link PasswordEncoderFactories#createDelegatingPasswordEncoder()}
     *
     * @param passwordEncoder must be an instance of one of the {@code PasswordEncoder}
     *                        types.
     */
    public void setPasswordEncoder(PasswordEncoder passwordEncoder) {
        Assert.notNull(passwordEncoder, "passwordEncoder cannot be null");
        this.passwordEncoder = passwordEncoder;
        this.userNotFoundEncodedPassword = null;
    }

    protected PasswordEncoder getPasswordEncoder() {
        return this.passwordEncoder;
    }

    public void setUserDetailsService(WebUserDetailsServiceImpl userDetailsService) {
        this.userDetailsService = userDetailsService;
    }

    protected WebUserDetailsServiceImpl getUserDetailsService() {
        return this.userDetailsService;
    }

    public void setUserDetailsPasswordService(UserDetailsPasswordService userDetailsPasswordService) {
        this.userDetailsPasswordService = userDetailsPasswordService;
    }

}

```

- security 配置。

```java
     /**
     * 身份认证接口
     */
    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.authenticationProvider(customerDaoAuthenticationProvider()).userDetailsService(userDetailsService).passwordEncoder(bCryptPasswordEncoder());
    }
... 省略...
    @Bean
    public CustomerDaoAuthenticationProvider customerDaoAuthenticationProvider() {
        CustomerDaoAuthenticationProvider customerDaoAuthenticationProvider = new CustomerDaoAuthenticationProvider();
        customerDaoAuthenticationProvider.setUserDetailsService(userDetailsService);
        return customerDaoAuthenticationProvider;
    }

```
- 启动时会把我的`CustomerDaoAuthenticationProvider`注册进来。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/971e15495d556532a6a1d14a2741adf3.png)
- 登录时，进入`parent`的`providers`。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/253e816d61937c909453eb42e3a72b11.png)
- 最后进入自定义的`CustomerDaoAuthenticationProvider#retrieveUser`方法。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b40a2ec589ec420b96e0b1bb8d1e4756.png)


## 参数都传入principal
- 我们调用`authenticationManager.authenticate`方法时传入`UsernamePasswordAuthenticationToken`。
- `UsernamePasswordAuthenticationToken`的第一个参数是`principal`，这个一般作为`用户名`，可以把全部参数传进去，在`loadUserByUsername`方法分割。就能拿到其他参数。
- 例如这样写。

```
  @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        String[] split = username.split(",");
        Users users = new Users();
        users.setName(split[0]);
         users.setXXX(split[1]);
        List<Users> usersList = usersService.selectUsersList(users);
        Assert.isEmpty(usersList, "没有这个用户");
        Users user = usersList.get(0);
        Assert.isTrue(Users.IS_LOCK_1.equals(user.getIsLock()), "用户已被锁定不能登录");
        return createLoginUser(user);
    }

    public WebLoginUserDetail createLoginUser(Users users) {
        WebLoginUserDetail webLoginUserDetail = mapperFacade.map(users,WebLoginUserDetail.class);
        return webLoginUserDetail;
    }
```
> 这个比较方便，不过用`username`字段做其他事情怪怪的。

## 参考
- [https://segmentfault.com/q/1010000040956141](https://segmentfault.com/q/1010000040956141)
- [https://blog.csdn.net/weixin_43909881/article/details/104925068](https://blog.csdn.net/weixin_43909881/article/details/104925068)