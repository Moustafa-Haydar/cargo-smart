<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\Role;
use App\Http\Requests\StoreRoleRequest;
use App\Services\Admin\RoleService;
use Illuminate\Http\Request;
use App\Traits\ResponseTrait;

use Illuminate\Support\Facades\Log;


class RoleController extends Controller
{
    use ResponseTrait;

    public function addRole(StoreRoleRequest $request)
    {
        Log::info('HIT addRole');

        $role = RoleService::addRole($request);
        return $this->responseJSON($role);
    }

    public function getAllRoles($id = null)
    {
        $roles = RoleService::getAllRoles($id);
        return $this->responseJSON($roles);
    }

}
