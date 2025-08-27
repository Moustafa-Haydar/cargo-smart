<?php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Common\AuthController;
use App\Http\Controllers\admin\UserController;
use App\Http\Middleware\EnsureAdmin;

Route::group(["prefix" => "v0.1"], function () {

    // UNAUTHENTICATED APIs (Public Endpoints)
    Route::group(["prefix" => "auth"], function () {

        Route::post("/login", [AuthController::class, "login"]);
        Route::get("/logout", [AuthController::class, "logout"]);

        Route::post("/forgot-password", [AuthController::class, "sendResetLink"]);
        Route::post("/reset-password", [AuthController::class, "resetPassword"]);


    });

    Route::group(["middleware" => "auth"], function () {

        // USER-SPECIFIC ENDPOINTS
        Route::group(["prefix" => "user"], function () {

            // add user-specific routes here


        });


        // ADMIN-SPECIFIC ENDPOINTS
        Route::group(["prefix" => "admin"], function () {
            Route::group(["middleware" => ['auth', EnsureAdmin::class]], function () {

                Route::post("/addUser", [UserController::class, "addUser"]);
                Route::get("/getAllUsers/{id?}", [UserController::class, "getAllUsers"]);

            });
        });

    });

});

?>