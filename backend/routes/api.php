<?php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

// import middlewares
use App\Http\Middleware\EnsureAdmin;

// import controllers
use App\Http\Controllers\Common\AuthController;
use App\Http\Controllers\admin\UserController;
use App\Http\Controllers\Admin\RoleController;

Route::group(["prefix" => "v0.1"], function () {

    // UNAUTHENTICATED APIs (Public Endpoints)
    Route::group(["prefix" => "auth"], function () {

        Route::post("/login", [AuthController::class, "login"]);
        Route::get("/logout", [AuthController::class, "logout"]);

        // Forgot and Reset Password Routes

        // User views form to request password reset link
        Route::get('/forgot-password', [AuthController::class, 'resetPasswordForm']);
        // User requests password reset link by providing username
        Route::post('/forgot-password', [AuthController::class, 'sendResetLink']);
        // User views form to reset password using the token from email
        Route::get('/reset-password/{token}', [AuthController::class, 'updatePasswordForm']);
        // User submits new password
        Route::post('/reset-password', [AuthController::class, 'updatePassword']);

    });

    Route::group(["middleware" => "auth"], function () {

        // USER-SPECIFIC ENDPOINTS
        Route::group(["prefix" => "user"], function () {

            // add user-specific routes here


        });


        // ADMIN-SPECIFIC ENDPOINTS
        Route::group(["prefix" => "admin"], function () {
            Route::group(["middleware" => ['auth', EnsureAdmin::class]], function () {

                // User Management
                Route::get("/getAllUsers/{id?}", [UserController::class, "getAllUsers"]);
                Route::post("/addUser", [UserController::class, "addUser"]);
                Route::post("/deleteUser", [UserController::class, "deleteUser"]);

                // Role Management
                Route::post("/addRole", [RoleController::class, "addRole"]);


                Route::get("/getAllRoles/{id?}", [RoleController::class, "getAllRoles"]);
                Route::post("/deleteUser", [RoleController::class, "deleteUser"]);


            });
        });

    });

});

?>